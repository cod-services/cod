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

from structures import *
from utils import *
import time
import sys

NAME="inspircd protocol module"
DESC="Handles login and protocol commands for inspircd"

def initModule(cod):
    cod.loginFunc = login
    cod.burstClient = burstClient
    cod.tsSecond = True

    cod.s2scommands["UID"] = [handleUID]
    cod.s2scommands["QUIT"] = [handleQUIT]
    cod.s2scommands["FJOIN"] = [handleSJOIN]
    cod.s2scommands["NICK"] = [handleNICK]
    cod.s2scommands["MODE"] = [handleMODE]
    cod.s2scommands["FHOST"] = [handleCHGHOST]
    cod.s2scommands["WHOIS"] = [handleWHOIS]
    cod.s2scommands["JOIN"] = [handleJOIN]
    cod.s2scommands["SID"] = [handleSID]
    cod.s2scommands["KILL"] = [handleKILL]
    cod.s2scommands["STATS"] = [handleSTATS]
    cod.s2scommands["PING"] = [handlePING]
    cod.s2scommands["SERVER"] = [handleSERVER]
    cod.s2scommands["ENDBURST"] = [handleENDBURST]
    cod.s2scommands["OPERTYPE"] = [handleOPERTYPE]

    cod.s2scommands["PRIVMSG"].append(handlePRIVMSG)

    cod.s2scommands["ENCAP"] = [nullCommand]
    cod.s2scommands["AWAY"] = [nullCommand]

def destroyModule(cod):
    del cod.s2scommands["UID"]
    del cod.s2scommands["QUIT"]
    del cod.s2scommands["FJOIN"]
    del cod.s2scommands["NICK"]
    del cod.s2scommands["MODE"]
    del cod.s2scommands["FHOST"]
    del cod.s2scommands["WHOIS"]
    del cod.s2scommands["NOTICE"]
    del cod.s2scommands["JOIN"]
    del cod.s2scommands["SID"]
    del cod.s2scommands["ENCAP"]
    del cod.s2scommands["KILL"]
    del cod.s2scommands["STATS"]
    del cod.s2scommands["PING"]
    del cod.s2scommands["SERVER"]
    del cod.s2scommands["ENDBURST"]
    del cod.s2scommands["OPERTYPE"]

    cod.s2scommands["PRIVMSG"].remove(handlePRIVMSG)

    del cod.s2scommands["AWAY"]

def rehash():
    pass

# Monkey-patch join because inspircd is weird
def join(cod, channel, client=None):
    if client is None:
        client = cod.client

    if channel not in cod.channels:
        cod.channels[channel] = Channel(channel, int(time.time()))

    channel = cod.channels[channel]

    client.channels.append(channel.name)

    cod.sendLine(":%s FJOIN %s %s + ,%s" % (cod.sid, channel.name, channel.ts,
        client.uid))

def burstClient(cod, nick, user, host, real, uid=None):
    if uid is None:
        uid = cod.getUID()

    cod.sendLine(":%s UID %s %d %s 127.0.0.1 %s %s 127.0.0.1 %d +kio :%s" %
            (cod.sid, uid, int(time.time()), nick, host,
                user, int(time.time()), real))

def login(cod):
    #>> SERVER services-dev.chatspike.net password 0 666 :Description here
    cod.sendLine("SERVER %s %s 0 %s :%s" %
            (cod.config["me"]["name"], cod.config["uplink"]["pass"],
                cod.sid, cod.config["me"]["desc"]))
    cod.sendLine("CAPAB START 1202")
    cod.sendLine("CAPAB CAPABILITIES :PROTOCOL=1202")
    cod.sendLine("CAPAB END")
    cod.sendLine(":%s BURST " % cod.sid + str(int(time.time())))
    cod.sendLine("ENDBURST")
    cod.bursted = True

def handleENDBURST(cod, line):
    cod.loadmod("admin")
    cod.loadmod("help")

    cod.join(cod.config["etc"]["staffchan"])
    cod.join(cod.config["etc"]["snoopchan"])

    cod.privmsg("NickServ", "IDENTIFY %s" % cod.config["me"]["servicespass"])

def nullCommand(cod, line):
    pass

def handleSERVER(cod, line):
    cod.sendLine(":%s BURST &d" % (cod.config["uplink"]["sid"], time.time()))

def handleUID(cod, line):
    #UID <uid> <age> <nick> <host> <dhost> <ident> <ip> <signon> +<modes> :realname
    # 0    1     2     3      4      5        6     7      8        9
    client = Client(line.args[2], line.args[0], line.args[1], line.args[8],
            line.args[5], line.args[4], line.args[6], "*", line.args[-1])

    cod.clients[client.uid] = client

def handleOPERTYPE(cod, line):
    cod.clients[line.source].isOper = True

def handleQUIT(cod, line):
    cod.clients.pop(source)

def handleJOIN(cod, line):
    # :<uuid> JOIN <#channel>{,<#channel>} <timestamp>
    channel = cod.channels[line.args[0]]

    channel.clientAdd(cod.clients[source])

def handlePART(cod, line):
    channel = cod.channels[line.args[0]]

    channel.clients.pop(source)

def handleSJOIN(cod, line):
    # :<sid> FJOIN <channel> <timestamp> +[<modes> {mode params}] [:<[statusmodes],uuid> {<[statusmodes],uuid>}]
    try:
        cod.channels[line.args[0]]
    except KeyError as e:
        cod.channels[line.args[0]] = Channel(line.args[0], line.args[1])
    finally:
        channel = cod.channels[line.args[0]]

        #Set channel modes
        channel.modes = line.args[2]

        #Join users to channel
        uids = line.args[-1].split()
        for uid in uids:
            #The only thing Spanning Tree gets right
            prefix, uid = uid.split(",")

            client = cod.clients[uid]

            channel.clientAdd(client, prefix)

def handleNICK(cod, line):
    cod.clients[source].nick = line.args[0]

def handleSID(cod, line):
    #SERVER <servername> <password> 0 <id> :<description>
    #:<local server id> SERVER <remote server> * <distance> <id> :<description>
    cod.servers[line.args[3]] = Server(line.args[3], line.args[0], 0,
            line.args[-1])

def handleMODE(cod, line):
    source = line.source
    extparam = line.args[-1]

    if extparam.find("o") != -1:
        if extparam[0] == "+":
            cod.clients[source].isOper = True
        else:
            cod.clients[source].isOper = False

def handleCHGHOST(cod, line):
    cod.clients[line.args[0]].host = line.args[1]

def handleWHOIS(cod, line):
    service = line.args[0]
    source = line.source

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

def handlePRIVMSG(cod, line):
    """
    Handle PRIVMSG
    """

    destination = line.args[0]
    source = cod.clients[line.source]
    line = line.args[-1]
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
        destination = cod.clients[destination]
        command = splitline[0].upper()

    #Guido, I am sorry.
    try:
        if source.isOper:
            for impl in cod.opercommands[command]:
                try:
                    if pm:
                        impl(cod, line, splitline, source, source)
                    else:
                        impl(cod, line, splitline, source, destination)
                except Exception as e:
                    cod.servicesLog("%s: %s" % (type(e), e.message))
                    continue
        else:
            raise KeyError

    except KeyError as e:
        for impl in cod.botcommands[command]:
            try:
                if pm:
                    impl(cod, line, splitline, source, source)
                else:
                    impl(cod, line, splitline, source, destination)
            except Exception as e:
                cod.servicesLog("%s: %s" % (type(e), e.message))
    except KeyError as e:
        return
    except Exception as e:
        cod.servicesLog("%s: %s" % (type(e), e.message))


def handleKILL(cod, line):
    """
    The KILL message, for when someone hasn't done something bad enough to be G:Lined
    """

    if line.args[0] != cod.client.uid:
        cod.clients.pop(line.args[0])
        return

    cod.sendLine(cod.client.burst())

    for channel in cod.client.channels:
        cod.join(channel)

    cod.servicesLog("KILL'd by %s " % line.source.nick)

def handleSTATS(cod, line):
    """
    The Server to Server STATS command. Does inspircd even support this?
    """

    source = line.source
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

def handlePING(cod, line):
    """
    Summary: if you get a ping, swap the last two params and send it back on
    the connection it came from. Don't ask why, just do.
    """

    args = (line.args[-1], line.args[-2])

    cod.sendLine(":%s PONG %s %s" % (cod.sid, args[0], args[1]))

