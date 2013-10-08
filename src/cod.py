#!/usr/bin/python

import socket
from structures import *
from commands import *

commands = {}

commands["EUID"] = handleEUID
commands["QUIT"] = handleQUIT
commands["SJOIN"] = handleSJOIN
commands["NICK"] = handleNICK
commands["BMASK"] = handleBMASK
commands["MODE"] = handleMODE
commands["TMODE"] = handleTMODE

class Cod():
    def __init__(self, host, port, password, SID, name, realname):
        self.link = socket.socket()

        self.clients = {}
        self.channels = {}
        self.servers = {}

        self.bursted = False

        self.link.connect((host, port))

        self.sid = SID
        self.name = name
        self.realname = realname

        self.sendLine("PASS %s TS 6 :%s" % (password, SID))
        self.sendLine("CAPAB :QS EX IE KLN UNKLN ENCAP TB SERVICES EUID EOPMOD MLOCK")
        self.sendLine("SERVER %s 1 :%s" % (name, realname))

        self.client = makeService("Cod", "fish", "blub.blub", "Cod!", SID + "CODFIS")

        self.clients[SID + "CODFIS"] = self.client

        self.sendLine(self.client.burst())

    def sendLine(self, line):
        print ">>> %s" % line
        self.link.send("%s\r\n" % line)

cod = Cod("127.0.0.1", 6667, "dev", "420", "ardreth.shadownet.int", "Cod fishy")
SNOOPCHAN = "#services"

for line in cod.link.makefile('r'):
    line = line.strip()

    print "<<< " + line
    splitline = line.split()

    if line[0] != ":":
        if line.split()[0] == "PING":
            cod.sendLine("PONG %s" % splitline[1:][0])

            if not cod.bursted:
                cod.bursted = True

                cod.sendLine(cod.client.join(cod.channels[SNOOPCHAN], True))
                cod.sendLine(cod.client.join(cod.channels["#cod"], True))

    else:
        source = splitline[0][1:]

        try:
            commands[splitline[1]](cod, line, splitline, source)
        except KeyError as e:
            continue

