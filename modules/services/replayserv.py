"""
Copyright (c) 2014, Sam Dodrill
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

from structures import makeService

DESC="Replays the last 5 lines of chat in a channel"

global my_client

def initModule(cod):
    global my_client

    cod.s2scommands["PRIVMSG"].append(handlePRIVMSG)
    cod.s2scommands["JOIN"].append(handleJOIN)

    my_client = makeService(cod.config["replay"]["nick"],
            cod.config["replay"]["user"],
            cod.config["replay"]["host"],
            cod.config["replay"]["gecos"], cod.getUID())

    cod.burstClient(cod, my_client)
    cod.join(cod.config["etc"]["snoopchan"], my_client)

def destroyModule(cod):
    cod.s2scommands["PRIVMSG"].remove(handlePRIVMSG)
    cod.s2scommands["JOIN"].remove(handleJOIN)

    cod.sendLine(my_client.quit())
    cod.clients.pop(my_client.uid)

def rehash():
    pass

def handlePRIVMSG(cod, line):
    if line.args[0][0] == "#":
        line.source = cod.clients[line.source]

        channel = cod.channels[line.args[0]]

        channel.addMessage(line)

def handleJOIN(cod, line):
    channame = ""

    if line.args[0][0] == "#":
        channame = line.args[0]
    elif line.args[1][0] == "#":
        channame = line.args[1]

    doReplay(cod, line.source, cod.channels[channame])

def doReplay(cod, client, channel):
    global my_client

    if len(channel.msgbuffer) == 0:
        return

    cod.notice(client, "Now replaying you the last 5 lines of chat in %s" % channel.name, my_client)

    for line in channel.msgbuffer:
        cod.notice(client, "<%s> %s" % (line.nick, line.message), my_client)

