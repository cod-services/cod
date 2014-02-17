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
        "gecos": "4chan Relay"
    },

"""

import htmllib
import threading
import time
import requests

from structures import makeService, makeClient

client = None
threads = {}

NAME="4ChanServ"
DESC="Live-feeds 4chan threads to a channel"

def initModule(cod):
    global client

    if "4chanserv" not in cod.config:
        cod.servicesLog("Need 4chanserv config")
        raise ImportError

    client = makeService(cod.config["4chanserv"]["nick"],
            cod.config["4chanserv"]["user"],
            cod.config["4chanserv"]["host"],
            cod.config["4chanserv"]["gecos"],
            cod.getUID())

    cod.clients[client.uid] = client
    client.channels.append(cod.config["etc"]["snoopchan"])

    cod.log("Bursting 4chanserv client")
    cod.burstClient(cod, client)
    cod.join(client.channels[0], client)

    cod.addHook("privmsg", handleCommands)

def destroyModule(cod):
    global client

    for thread in threads:
        threads[thread].slay()

    cod.sendLine(client.quit())
    cod.clients.pop(client.uid)

    cod.delHook("privmsg", handleCommands)

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

    if target.uid != client.uid:
        return

    command = splitline[0].upper()

    print command

    if command == "MONITOR":
        board, target, thread = None, None, None

        try:
            board = splitline[1]
            thread = splitline[2]
            target = splitline[3]
        except IndexError:
            cod.notice(line.args[0], "Insufficient parameters.", client)

        #Sanity check
        if len(board) > 4:
            cod.notice(line.args[0], "/%s/ is not a board on 4chan.", client)

        cod.servicesLog("%s MONITOR:/%s/%s to %s" % (line.source.nick, board, thread, target), client)

        tm = ThreadMonitor(cod, target, board, thread)
        tm.start()

        threads[board+thread] = tm

    elif command == "DEMONITOR":
        try:
            board = splitline[1]
            thread = splitline[2]
        except IndexError:
            cod.notice(line.args[0], "Insufficient parameters.", client)

        victim = board+thread

        if victim in threads:
            target = threads[victim].target
            threads[victim].slay()

            cod.servicesLog("%s MONITOR:STOP:/%s/%s to %s" %
                    (line.source.nick, board, thread, target), client)

        else:
            cod.notice(line.source.uid, "could not find /%s/%s in thread monitor list" %
                    (board, thread), client)

    elif command == "HELP":
        cod.notice(line.source.uid, "HELP:", client)
        cod.notice(line.source.uid, "MONITOR:   - monitors 4chan <board> <thread> to <channel>", client)
        cod.notice(line.source.uid, "DEMONITOR: - disables monitoring of a <board> <thread>", client)

    else:
        cod.notice(line.source.uid, "Invalid command. Use /msg %s HELP or join %s for more help" %
                (client.nick, cod.config["etc"]["helpchan"]), client)

def unescape(comment):
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(comment)
    return p.save_end()

class ThreadMonitor(threading.Thread):
    def __init__(self, cod, target, board, threadid, interval=15):
        global client

        threading.Thread.__init__(self)

        self.cod = cod
        self.board = board
        self.target = cod.channels[target]
        self.threadid = threadid
        self.interval = interval
        self.lastpostid = 0
        self.dying = False

        nick = "[4CS]\%s\%s" % (board, threadid)

        self.client = makeClient(nick, "monitor", "boards.4chan.org",
                "4ChanServ monitor for /%s/%s to %s" % (board, threadid, target), cod.getUID())
        cod.burstClient(cod, self.client)
        cod.protocol.join_client(self.client, self.target)
        cod.protocol.join_client(self.client, cod.channels[cod.config["etc"]["snoopchan"]])

        cod.clients[self.client.uid] = self.client

        try:
            self.checkThread()
        except ValueError:
            cod.privmsg(self.client, self.target, "Thread %s is invalid" % self.threadid)
        except Exception as e:
            cod.servicesLog("Monitor on thread /%s/%s failed for %s and %s" %\
                    (self.board, self.threadid, type(e), e.message), client)

    def checkThread(self):
        json = requests.get("http://api.4chan.org/%s/res/%s.json" %
                (self.board, self.threadid)).json()

        newpostid = json["posts"][-1]["no"]

        if self.lastpostid == 0:
            subject = ""

            if "sub" not in json["posts"][0]:
                subject = json["posts"][0]["com"].split("<br>")[0]
                subject = remove_html_markup(subject)
                subject = unescape(subject)
            else:
                subject = json["posts"][0]["sub"]

            self.cod.protocol.privmsg(self.client, self.target, "Subject for /%s/%s: %s" % (self.board,
                self.threadid, subject))

        if newpostid != self.lastpostid and self.lastpostid != 0:
            newposts = filter((lambda x: x["no"] > self.lastpostid), json["posts"])

            for post in newposts:
                try:
                    string = "[%s] " % post["no"]
                    if "name" in post:
                        string += "%s " % unescape(remove_html_markup(post["name"]))
                    else:
                        string += "Anonymous "

                    if "filename" in post:
                        string += "posted %s%s and " % (post["filename"], post["ext"])
                    if "com" in post:
                        comment = post["com"].replace("<br>", " \ ")
                        comment = remove_html_markup(comment)
                        comment = unescape(comment)

                        string += "commented: %s" % comment
                    else:
                        string += "did not comment."

                    self.cod.protocol.privmsg(self.client, self.target, string)
                except UnicodeError:
                    self.cod.protocol.privmsg(self.client, self.target,
                            "Post with id %s could not be read: Unicode use?" % post["no"])
                    self.cod.servicesLog("Unicode error on post %s" % post["no"], self.client)

        self.lastpostid = newpostid

    def slay(self):
        self.dying = True

        self.cod.protocol.quit(self.client, "Monitor stopped.")
        del self.cod.clients[self.client.uid]

    def run(self):
        while not self.dying:
            try:
                self.checkThread()
            except ValueError as e:
                self.slay()
                self.cod.protocol.privmsg(client, self.target, "Montioring stopped for /%s/%s: %s %s. Did the thread die?" %\
                        (self.board, self.threadid, type(e), e.message))
            except Exception as e:
                self.slay()
                self.cod.protocol.privmsg(client, self.target, "Thread monitoring for /%s/%s stopped for an unknown reason." %\
                        (self.board, self.threadid))
                self.cod.servicesLog(client, "Monitoring broken for /%s/%s to %s because %s %s" %\
                        (self.board, self.threadid, self.target, type(e), e.message), client)

            for n in range(self.interval):
                time.sleep(1)

                if self.dying:
                    break

