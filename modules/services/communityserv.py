"""
Copyright (c) 2013, Sam Dodrill
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

NAME="Community Service"
DESC="A place for communities to register information about themselves"

from structures import *
from utils import *

global client

def initModule(cod):
    global client

    client = makeService(cod.config["commserv"]["nick"], cod.config["commserv"]["user"],
            cod.config["commserv"]["host"], cod.config["commserv"]["gecos"],
            cod.getUID())

    cod.s2scommands["PRIVMSG"].append(handleMessages)

    initDBTable(cod, "Communities",
            "Id INTEGER PRIMARY KEY, Name TEXT, Url TEXT, Channel TEXT, Description TEXT")

    cod.clients[client.uid] = client

    cod.sendLine(client.burst())

    cod.log("Bursting FAQ client", "!!!")

    cod.sendLine(client.join(cod.channels[cod.config["etc"]["snoopchan"]]))
    cod.sendLine(client.join(cod.channels[cod.config["etc"]["helpchan"]]))
    cod.sendLine(client.join(cod.channels[cod.config["etc"]["lobbychan"]]))

    if cod.config["commserv"]["autojoin"]:
        rows = lookupDB(cod, "Communities")

        if rows == []:
            return

        for row in rows:
            cod.join(row[3], client)

def destroyModule(cod):
    global client

    cod.sendLine(client.quit())
    cod.clients.pop(client.uid)

    cod.s2scommands["PRIVMSG"].remove(handleMessages)

def rehash():
    pass

def handleMessages(cod, line):
    global client

    if line.args[0] != client.uid:
        return

    splitline = line.args[-1].split()

    if splitline[0] == "LIST":
        listComms(cod, cod.clients[line.source])
    elif splitline[0] == "ADD":
        addcommunity(cod, cod.clients[line.source], splitline[1:])

def listComms(cod, uclient, by=None):
    global client

    comms = lookupDB(cod, "Communities")

    if comms == []:
        cod.sendLine(client.notice(uclient.uid, "No communities added to the list"))
        return

    for comm in comms:
        cod.sendLine(client.notice(uclient.uid, "%d: %s: <%s> %s - %s" % comm, client))

def addcommunity(cod, uclient, args):
    global client

    if len(args) < 4:
        cod.sendLine(client.notice(uclient.uid, "Need more params"))
        return

    desc = " ".join(args[4:])
    name = args[0]

    pass

