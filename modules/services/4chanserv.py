"""
Copyright (c) 2014, Xe
All rights reserved.

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

    1. The origin of this software must not be misrepresented; you must not
    claim that you wrote the original software. If you use this software
    in a product, an acknowledgment in the product documentation would be
    appreciated but is not required.

    2. Altered source versions must be plainly marked as such, and must not be
    misrepresented as being the original software.

    3. This notice may not be removed or altered from any source
    distribution.
"""

"""
To use this module, add a 4chanserv block to your config.json. The one I use
is below:

    "4chanserv": {
        "nick": "4ChanServ",
        "user": "moot",
        "host": "4chan.org",
        "gecos": "4chan Relay",
        "prefix": "<"
    },

"""

import htmllib
import threading
import time
import requests

from structures import makeService

client = None
threads = {}

NAME="4ChanServ"
DESC="Live-feeds 4chan threads to a channel"

def initModule(cod):
    global client

    client = makeService(cod.config["4chanserv"]["nick"], cod.config["4chanserv"]["user"],
            cod.config["4chanserv"]["host"], cod.config["4chanserv"]["gecos"],
            cod.getUID())

    cod.clients[client.uid] = client
    client.channels.append(cod.config["etc"]["snoopchan"])

    cod.log("Bursting 4chanserv client")
    cod.burstClient(cod, client)
    cod.join(client.channels[0], client)

    cod.addHook("chanmsg", handleCommands)

def destroyModule(cod):
    global client

    for thread in threads:
        threads[thread].slay()

    cod.sendLine(client.quit())
    cod.clients.pop(client.uid)

# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out

def handleCommands(cod, target, line):
    global client
    global threads

    splitline = line.args[-1].split()
    channel = line.args[0]

    if channel not in client.channels:
        return

    if splitline[0][0] == cod.config["4chanserv"]["prefix"]:
        command = splitline[0][1:].upper()

        if not line.source.isOper:
            return

        if command == "JOIN":
            channel = splitline[1]

            if channel in cod.channels:
                cod.join(channel, client)
                cod.servicesLog("%s JOIN:%s" % (line.source.nick, channel), client)

            else:
                cod.notice("I don't know about %s" % (channel), client)

            return

        elif command == "MONITOR":
            board = splitline[1]
            thread = splitline[2]
            channel = splitline[3]

            #Sanity check
            if len(board) > 4:
                cod.notice(line.args[0], "/%s/ is not a board on 4chan.", client)

            cod.notice(channel, "Now monitoring /%s/%s" % (board, thread), client)
            cod.servicesLog("%s MONITOR:/%s/%s to %s" % (line.source.nick, board, thread, channel))

            tm = ThreadMonitor(cod, channel, board, thread)
            tm.start()

            threads[board+thread] = tm

        elif command == "DEMONITOR":
            board = splitline[1]
            thread = thread = splitline[2]

            if board+thread in threads:
                target = threads[board+thread].target
                threads[board+thread].slay()

                cod.notice(target, "Stopped monitoring /%s/%s at the request of %s" %
                        (board, thread, line.source.nick), client)
                cod.servicesLog("%s MONITOR:STOP:/%s/%s to %s" %\
                        (line.source.nick, board, thread, target), client)

            else:
                cod.notice(line.source.uid, "could not find /%s/%s in thread monitor list" %
                        (board, thread), client)

        elif command == "HELP":
            cod.notice(line.source.uid, "HELP:", client)
            cod.notice(line.source.uid, "JOIN: <channel> - Joins a channel", client)
            cod.notice(line.source.uid, "MONITOR: <board> <thread> <channel> - monitors 4chan <board> <thread> to #channel", client)
            cod.notice(line.source.uid, "DEMONITOR: <board> <thread> - disabled monitoring to a channel", client)

def unescape(comment):
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(comment)
    return p.save_end()

class ThreadMonitor(threading.Thread):
    def __init__(self, cod, target, board, threadid, interval=60):
        global client

        threading.Thread.__init__(self)

        self.cod = cod
        self.board = board
        self.target = target
        self.threadid = threadid
        self.interval = interval
        self.lastpostid = 0
        self.dying = False

        try:
            self.checkThread()
        except ValueError:
            cod.notice(target.name, "Thread %s is invalid" % self.threadid,
                    client)
        except Exception as e:
            cod.servicesLog("Monitor on thread /%s/%s failed for %s and %s" %\
                    (self.board, self.threadid, type(e), e.message), client)

    def checkThread(self):
        json = requests.get("http://api.4chan.org/%s/res/%s.json" %
                (self.board, self.threadid)).json()

        newpostid = json["posts"][-1]["no"]

        self.cod.log("/%s/%s: oldpost=%s, newpostid=%s" %
                (self.board, self.threadid, self.lastpostid, newpostid), "4CS")

        if newpostid != self.lastpostid and self.lastpostid != 0:
            newposts = filter((lambda x: x["no"] > self.lastpostid), json["posts"])

            for post in newposts:
                string = "/%s/%s: New post: " % (self.board, self.threadid)
                if "name" in post:
                    string += "%s " % post["name"]
                else:
                    string += "Anonymous "

                string += "(%s) " % post["no"]

                if "filename" in post:
                    string += "posted %s%s and " % (post["filename"], post["ext"])
                if "com" in post:
                    comment = post["com"].replace("<br>", " \ ")
                    comment = remove_html_markup(comment)
                    comment = unescape(comment)

                    string += "commented: %s" % comment
                else:
                    string += "did not comment."

                self.cod.notice(self.target, string, client)

        self.lastpostid = newpostid

    def slay(self):
        self.dying = True

    def run(self):
        while not self.dying:
            try:
                self.checkThread()
            except ValueError as e:
                self.slay()
                self.cod.notice(self.target, "Montioring stopped for /%s/%s: %s %s. Did the thread die?" %\
                        (self.board, self.threadid, type(e), e.message))
            except Exception as e:
                self.slay()
                self.cod.notice(self.target, "Thread monitoring for /%s/%s stopped for an unknown reason." %\
                        (self.board, self.threadid), client)
                self.cod.servicesLog("Monitoring broken for /%s/%s to %s because %s %s" %\
                        (self.board, self.threadid, self.target, type(e), e.message), client)

            for n in range(self.interval):
                time.sleep(1)

                if self.dying:
                    break

