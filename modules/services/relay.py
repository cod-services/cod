"""
Copyright (c) 2013-2014, Sam Dodrill
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

import socket
from niilib.message import IRCMessage
from structures import Client, Channel, makeClient

NAME="Relay"
DESC="IRC channel relay bot"

class FakeClient:
    def __init__(self, string):
        self.nick = string.split("!")[0]
        self.user = string.split("!")[1].split("@")[0]
        self.host = string.split("@")[1]

class Relay:
    def __init__(self, cod, host, port, channel):
        self.cod = cod
        self.link = socket.socket()
        self.host = host
        self.port = port
        self.channel = Channel(channel, 0)
        self.clients = {}
        self.prefixes = {}
        self.isupp_prefixes = {}

        self.buf = ""

    def relay_chanmsg(self, cod, target, line):
        if line.source.nick.endswith("`"):
            return

        if self.channel.name == target.name:
            self.send_line("PRIVMSG %s :<-%s> %s" %
                    (self.channel, line.source.nick, line.args[-1]))

    def send_line(self, line):
        self.cod.log(line, "RY>")
        self.link.send("%s\r\n" % line)

    def join(self, channel=None):
        channel = self.channel.name if channel == None else channel

        self.send_line("JOIN %s" % channel)
        self.send_line("WHO %s" % channel)

    def handlePRIVMSG(self, line):
        message = line.args[-1]
        client = self.clients[line.source.nick]

        channel = self.cod.channels[self.channel.name]

        line.source = client

        self.cod.protocol.privmsg(client, self.channel, message)
        self.cod.runHooks("chanmsg", [channel, line])

    def handlePING(self, line):
        self.send_line("PONG :%s" % " ".join(line.args))

    def handle352(self, line):
        "WHO reply to a channel"

        nick = line.args[5]
        user = line.args[2]
        host = line.args[3]

        if nick not in self.clients:
            channel = self.cod.channels[line.args[1]]

            client = makeClient(nick + "`", user, host, line.args[-1], self.cod.getUID())

            self.cod.protocol.add_client(client)
            self.cod.clients[client.uid] = client

            channel.clientAdd(client)
            self.cod.protocol.join_client(client, channel)

            self.clients[nick] = client

    def handleJOIN(self, line):
        self.send_line("WHO %s" % line.source.nick)

    def handleNICK(self, line):
        pass
        # Change nickname, update references

        client = self.clients[line.source.nick]

        nick = line.args[-1] + "`"

        client.nick = nick
        self.cod.clients[client.uid].nick = nick

        self.cod.protocol.change_nick(client, client.nick)
        self.clients[client.nick] = client

    def handleKICK(self, line):
        kicker = self.clients[line.source.nick]
        client = client = self.clients[line.args[1]]

        self.cod.protocol.quit(client, "Kicked by %s: %s" % (kicker.nick, line.args[-1]))

        del self.clients[client.nick[:-1]]
        del self.cod.clients[client.uid]

    def handle376(self, line):
        self.join(self.channel)

    def handleQUIT(self, line):
        client = self.clients[line.source.nick]

        self.cod.protocol.quit(client, line.args[-1])

        del self.clients[client.nick[:-1]]
        del self.cod.clients[client.uid]

    def go(self):
        self.cod.socks.append(self.link)
        self.cod.sockhandlers[self.link] = self.process
        self.link.connect((self.host, self.port))

        self.cod.addHook("chanmsg", self.relay_chanmsg)

        self.send_line("NICK %s" % self.cod.config["relay"]["nick"])
        self.send_line("USER {0} {0} {0} :{0}".format(self.cod.config["relay"]["nick"]))

    def stop(self):
        self.cod.socks.remove(self.link)
        del self.cod.sockhandlers[self.link]
        self.cod.delHook("chanmsg", self.relay_chanmsg)

        for client in self.clients:
            client = self.clients[client]
            self.cod.protocol.quit(client, "Relay stopped")
            del self.cod.clients[client.uid]

        self.send_line("QUIT :Service Unloaded.")
        self.link.close()

    def process(self, args):
        tbuf = self.link.recv(2048)
        tbuf = self.buf + tbuf

        lines = tbuf.split("\r\n")

        self.buf = lines[-1]
        lines = lines[:-1]

        self.processLines(lines)

    def processLines(self, lines):
        for line in lines:
            self.cod.log(line, "RL<")

            line = IRCMessage(line)
            if line.source != None and "!" in line.source:
                line.source = FakeClient(line.source)

            if line.verb == "PING":
                self.handlePING(line)
            elif line.verb == "PRIVMSG":
                self.handlePRIVMSG(line)
            elif line.verb == "JOIN":
                self.handleJOIN(line)
            elif line.verb == "352":
                self.handle352(line)
            elif line.verb == "376":
                self.handle376(line)
            elif line.verb == "PART" or line.verb == "QUIT":
                self.handleQUIT(line)
            elif line.verb == "NICK":
                self.handleNICK(line)
            elif line.verb == "KICK":
                self.handleKICK(line)

global relay
relay = None

def initModule(cod):
    global relay

    relay = Relay(cod, cod.config["relay"]["host"], cod.config["relay"]["port"],
            cod.config["relay"]["channel"])

    relay.go()

def destroyModule(cod):
    global relay

    relay.stop()

