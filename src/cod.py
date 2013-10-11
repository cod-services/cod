#!/usr/bin/python

VERSION = "0.3"

import config
import socket
import os
import sys
from structures import *
from mpd import MPDClient

class Cod():
    def __init__(self):
        self.version = VERSION

        self.link = socket.socket()

        self.clients = {}
        self.channels = {}
        self.servers = {}
        self.modules = {}

        self.s2scommands = {"PRIVMSG": []}
        self.botcommands = {}

        self.bursted = False

        self.config = config.Config("config.json").config

        if self.config["etc"]["production"]:
            print "--- Forking to background"

            try:
                pid = os.fork()
            except OSError, e:
                raise Exception, "%s [%d]" % (e.strerror, e.errno)

            if (hasattr(os, "devnull")):
                REDIRECT_TO = os.devnull
            else:
                REDIRECT_TO = "/dev/null"

            if (pid == 0):
                os.setsid()
            else:
                os._exit(0)

        for module in self.config["modules"]["coremods"]:
            self.loadmod(module)

        for module in self.config["modules"]["optionalmods"]:
            self.loadmod(module)

        self.log("Establishing connection to uplink")

        self.link.connect((self.config["uplink"]["host"], self.config["uplink"]["port"]))

        self.log("done")

        self.log("Sending credentials to remote IRC server")

        self.sendLine("PASS %s TS 6 :%s" %
                (self.config["uplink"]["pass"], self.config["uplink"]["sid"]))
        self.sendLine("CAPAB :QS EX IE KLN UNKLN ENCAP SERVICES EUID EOPMOD")
        self.sendLine("SERVER %s 1 :%s" %
                (self.config["me"]["name"], self.config["me"]["desc"]))

        self.log("done")
        self.log("Creating and bursting client")

        self.client = makeService(self.config["me"]["nick"],
                self.config["me"]["user"], self.config["me"]["host"],
                self.config["me"]["desc"], self.config["uplink"]["sid"] + "CODFIS")

        self.clients[self.config["uplink"]["sid"] + "CODFIS"] = self.client

        self.sendLine(self.client.burst())

        self.log("done")

        self.privmsg("NickServ", "ID %s %s" % \
                (self.config["me"]["acctname"], self.config["me"]["nspass"]))

        self.sendLine(":%s ENCAP * SNOTE s :Cod initialized" % self.config["uplink"]["sid"])
        self.log("Cod initialized", "!!!")

    def loadmod(self, modname):
        self.log("Trying to load module %s" % modname)
        oldpath = list(sys.path)
        sys.path.insert(0, "src/modules/")
        sys.path.insert(1, "src/modules/core")

        self.modules["modules/"+modname] = __import__(modname)
        self.modules["modules/"+modname].initModule(self)

        self.log("Module %s loaded" % modname)

        sys.path[:] = oldpath

    def unloadmod(self, modname):
        self.log("Trying to unload module %s" % modname)

        self.modules["modules/"+modname].destroyModule(self)
        del self.modules["modules/"+modname]

        self.log("Module %s unloaded" % modname)

    def rehash(self):
        self.log("Rehashing...")

        for module in self.modules:
            name = module.split("/")[1]
            self.unloadmod(name)
            self.loadmod(name)

        self.config = config.Config("config.json").config

        if self.config["mpd"]["enable"]:
            self.mpd = MPDClient()
            self.mpd.timeout = 10
            self.mpd.idletimeout = None
            self.mpd.connect(self.config["mpd"]["host"], self.config["mpd"]["port"])

        self.sendLine(self.client.quit())
        self.sendLine(self.client.burst())

        for channel in cod.config["me"]["channels"]:
            cod.join(channel, False)

        self.log("Rehash complete")

    def sendLine(self, line):
        if self.config["etc"]["debug"]:
            self.log(line, ">>>")

        self.link.send("%s\r\n" % line)

    def privmsg(self, target, line):
        self.sendLine(":%s PRIVMSG %s :%s" % (self.client.uid, target, line))

    def notice(self, target, line):
        self.sendLine(":%s NOTICE %s :%s" % (self.client.uid, target, line))

    def join(self, channel, op=False):
        channel = self.channels[channel]

        self.sendLine(self.client.join(channel, op))

    def snote(self, line, mask="d"):
        self.sendLine(":%s ENCAP * SNOTE %s :%s" % \
                (self.config["uplink"]["sid"], mask, line))

    def log(self, message, prefix="---"):
        if not self.config["etc"]["production"]:
            print prefix, message

        if self.bursted and prefix == "---":
            self.snote("%s" % (message))

    def servicesLog(self, line):
        self.privmsg(self.config["etc"]["snoopchan"], line)

    def findClientByNick(self, nick):
        for client in self.clients:
            if cod.clients[client].nick == nick:
                return cod.clients[client]

print "!!! Cod %s starting up" % VERSION

cod = Cod()

#start up

for line in cod.link.makefile('r'):
    line = line.strip()

    if cod.config["etc"]["debug"]:
        cod.log(line, "<<<")

    splitline = line.split()

    if line[0] != ":":
        if line.split()[0] == "PING":
            cod.sendLine("PONG %s" % splitline[1:][0])

            if not cod.bursted:
                cod.bursted = True

                for channel in cod.config["me"]["channels"]:
                    cod.join(channel)

    else:
        source = splitline[0][1:]

        try:
            for impl in cod.s2scommands[splitline[1]]:
                impl(cod, line, splitline, source)
        except KeyError as e:
            pass

