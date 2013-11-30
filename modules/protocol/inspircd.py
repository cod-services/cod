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

from structures import *
from utils import *
import time
import sys

NAME="inspircd protocol module"
DESC="Handles login and protocol commands for inspircd"

def initModule(cod):
    cod.loginFunc = login
    cod.burstClient = burstClient

    cod.s2scommands["UID"] = [handleUID]
    cod.s2scommands["QUIT"] = [handleQUIT]
    cod.s2scommands["FJOIN"] = [handleSJOIN]
    cod.s2scommands["NICK"] = [handleNICK]
    cod.s2scommands["BMASK"] = [handleBMASK]
    cod.s2scommands["MODE"] = [handleMODE]
    cod.s2scommands["CHGHOST"] = [handleCHGHOST]
    cod.s2scommands["WHOIS"] = [handleWHOIS]
    cod.s2scommands["JOIN"] = [handleJOIN]
    cod.s2scommands["SID"] = [handleSID]
    cod.s2scommands["KILL"] = [handleKILL]
    cod.s2scommands["STATS"] = [handleSTATS]
    cod.s2scommands["PING"] = [handlePING]
    cod.s2scommands["SERVER"] = [handleSERVER]

    cod.s2scommands["PRIVMSG"].append(handlePRIVMSG)

    cod.s2scommands["AWAY"] = [nullCommand]

def destroyModule(cod):
    del cod.loginFunc
    cod.loginFunc = None

    del cod.s2scommands["UID"]
    del cod.s2scommands["QUIT"]
    del cod.s2scommands["FJOIN"]
    del cod.s2scommands["NICK"]
    del cod.s2scommands["BMASK"]
    del cod.s2scommands["MODE"]
    del cod.s2scommands["CHGHOST"]
    del cod.s2scommands["WHOIS"]
    del cod.s2scommands["NOTICE"]
    del cod.s2scommands["JOIN"]
    del cod.s2scommands["SID"]
    del cod.s2scommands["ENCAP"]
    del cod.s2scommands["KILL"]
    del cod.s2scommands["STATS"]
    del cod.s2scommands["PING"]
    del cod.s2scommands["SERVER"]

    cod.s2scommands["PRIVMSG"].remove(handlePRIVMSG)

    del cod.s2scommands["AWAY"]

def rehash():
    pass

def burstClient(cod, nick, user, host, real, uid):
    cod.sendLine(":%s UID %s %d %s 127.0.0.1 %s %s 127.0.0.1 %d +kio :%s" %
            (cod.config["uplink"]["sid"], uid, int(time.time()), nick, host,
                user, int(time.time()), real))

def login(cod):
    #>> SERVER services-dev.chatspike.net password 0 666 :Description here
    cod.sendLine("SERVER %s %s 0 %s :%s" %
            (cod.config["me"]["name"], cod.config["uplink"]["pass"],
                cod.config["uplink"]["sid"], cod.config["me"]["desc"]))
    cod.sendLine("CAPAB START 1202")
    cod.sendLine("CAPAB CAPABILITIES :PROTOCOL=1202")
    cod.sendLine("CAPAB END")
    cod.sendLine(":%s BURST " % cod.config["uplink"]["sid"] + str(int(time.time())))
    cod.sendLine("ENDBURST")

def nullCommand(cod, line, splitline, source):
    pass

def handleSERVER(cod, line, splitline, source):
    cod.sendLine(":%s BURST &d" % (cod.config["uplink"]["sid"], time.time()))

def handleUID(cod, line, splitline, source):
    #UID <uid> <age> <nick> <host> <dhost> <ident> <ip> <signon> +<modes> :realname
    # 0    1     2     3      4      5        6     7      8        9
    client = Client(splitline[3], splitline[1], splitline[2], splitline[9],
            splitline[6], splitline[5], splitline[7], "*", ":".join(line.split(":")[2:]))

    cod.clients[client.uid] = client

def handleQUIT(cod, line, splitline, source):
    cod.clients.pop(source)

def handleJOIN(cod, line, splitline, source):
    channel = cod.channels[splitline[3]]

    channel.clientAdd(cod.clients[source])

def handlePART(cod, line, splitline, source):
    channel = cod.channels[splitline[3]]

    channel.clients.pop(source)

def handleSJOIN(cod, line, splitline, source):
    try:
        cod.channels[splitline[3]]
    except KeyError as e:
        cod.channels[splitline[3]] = Channel(splitline[3], splitline[2])
    finally:
        #Set channel modes
        cod.channels[splitline[3]].modes = splitline[4]

        #Join users to channel
        uids = line.split(":")[2].split(" ")
        for uid in uids:
            #Extremely pro implementation

            prefix = uid[:-9]
            uid = uid[-9:]

            client = cod.clients[uid]

            cod.channels[splitline[3]].clientAdd(client, prefix)

def handleNICK(cod, line, splitline, source):
    cod.clients[source].nick = splitline[2]

def handleSID(cod, line, splitline, source):
    cod.servers[source] = Server(source, splitline[2], splitline[3], ":".join(line.split(":")[2:]))

def handleBMASK(cod, line, splitline, source):
    list = splitline[4]

    #The channel will be a valid channel
    channel = cod.channels[splitline[3]]

    channel.lists[list].append([n for n in line.split(":")[2].split(" ")])

def handleMODE(cod, line, splitline, source):
    extparam = line.split(":")[2]

    if extparam.find("o") != -1:
        if extparam[0] == "+":
            cod.clients[source].isOper = True
        else:
            cod.clients[source].isOper = False

def handleCHGHOST(cod, line, splitline, source):
    cod.clients[splitline[2]].host = splitline[3]

def handleWHOIS(cod, line, splitline, source):
    service = splitline[2]

    client = cod.clients[service]

    cod.sendLine(":{0} 311 {1} {2} {3} {4} * :{5}".format(
        cod.config["uplink"]["sid"], source, client.nick, client.user,
                client.host, client.gecos))
    cod.sendLine(":{0} 312 {1} {2} {3} :{4}".format(
        cod.config["uplink"]["sid"], source, client.nick, cod.config["me"]["name"],
        cod.config["me"]["desc"]))
    cod.sendLine(":{0} 313 {1} {2} :is a Network Service".format(
        cod.config["uplink"]["sid"], source, client.nick))
    cod.sendLine(":{0} 318 {1} {2} :End of /WHOIS list.".format(
        cod.config["uplink"]["sid"], source, client.nick))

def handlePRIVMSG(cod, line, splitline, source):
    destination = splitline[2]
    line = ":".join(line.split(":")[2:])
    splitline = line.split()

    command = ""
    pm = True

    if destination[0] == "#":
        if destination not in cod.client.channels:
            return
        try:
            if line[0] == cod.config["me"]["prefix"]:
                command = splitline[0].upper()
                command = command[1:]
                pm = False
        except IndexError as e:
            return

    elif destination != cod.client.uid and pm:
        return

    else:
        command = command = splitline[0].upper()

    try:
        for impl in cod.botcommands[command]:
            try:
                if pm:
                    impl(cod, line, splitline, source, source)
                else:
                    impl(cod, line, splitline, source, destination)
            except Exception as e:
                cod.servicesLog("%s: %s" % (type(e), e))
    except KeyError as e:
        pass

def handleKILL(cod, line, splitline, source):
    if splitline[2] != cod.client.uid:
        return

    cod.sendLine(cod.client.burst())

    for channel in cod.client.channels:
        cod.join(channel)

    cod.servicesLog("KILL'd by %s " % cod.clients[source].nick)
    
def handleSTATS(cod, line, splitline, source):
    if splitline[2] == "v":
        cod.notice(source, "Cod version %s" % cod.version)

    elif splitline[2] == "c":
        cod.notice(source, "%d clients in ram" % len(cod.clients))

    elif splitline[2] == "C":
        cod.notice(source, "%d channels in ram" % len(cod.channels))

    elif splitline[2] == "m":
        cod.notice(source, "%d modules loaded" % len(cod.modules))

    elif splitline[2] == "M":
        cod.notice(source, "%d protocol commands loaded" % len(cod.s2scommands))
        cod.notice(source, "%d bot commands loaded" % len(cod.botcommands))
    else:
        cod.notice(source, "Stats commands: [v]ersion, [c]lients, [C]hannels, [m]modules, co[M]mands")

    cod.notice(source, "End of /STATS report")

def handlePING(cod, line, splitline, source):
    cod.sendLine(":%s PONG %s :%s" %
            (cod.config["uplink"]["sid"], cod.config["me"]["name"],
                source))

