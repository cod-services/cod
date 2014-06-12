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

import sys
import traceback

from channel    import Ban, ChanUser, Channel
from modes      import *
from structures import Client, Server
from utils      import *
from protocol   import TS6ServerConn

NAME="TS6 protocol module"
DESC="Handles login and protocol commands for TS6 servers"

sidhack = ""

def initModule(cod):
    cod.loginFunc = login
    cod.burstClient = burstClient
    cod.tsSecond = False
    cod.protocol = TS6ServerConn(cod)

    cod.s2scommands["EUID"] = [handleEUID]
    cod.s2scommands["QUIT"] = [handleQUIT]
    cod.s2scommands["PART"] = [handlePART]
    cod.s2scommands["SJOIN"] = [handleSJOIN]
    cod.s2scommands["NICK"] = [handleNICK]
    cod.s2scommands["BMASK"] = [handleBMASK]
    cod.s2scommands["MODE"] = [handleMODE]
    cod.s2scommands["CHGHOST"] = [handleCHGHOST]
    cod.s2scommands["ENCAP"] = [encapSU]
    cod.s2scommands["WHOIS"] = [handleWHOIS]
    cod.s2scommands["JOIN"] = [handleJOIN]
    cod.s2scommands["SID"] = [handleSID]
    cod.s2scommands["KILL"] = [handleKILL]
    cod.s2scommands["STATS"] = [handleSTATS]
    cod.s2scommands["PING"] = [handlePING]
    cod.s2scommands["ERROR"] = [handleERROR]
    cod.s2scommands["SQUIT"] = [handleSQUIT]
    cod.s2scommands["TMODE"] = [handleTMODE]
    cod.s2scommands["SID"] = [handleSID]

    cod.s2scommands["PRIVMSG"].append(handlePRIVMSG)

def destroyModule(cod):
    del cod.loginFunc
    cod.loginFunc = None
    del cod.burstClient
    cod.burstClient = None

    del cod.s2scommands["EUID"]
    del cod.s2scommands["QUIT"]
    del cod.s2scommands["PART"]
    del cod.s2scommands["SJOIN"]
    del cod.s2scommands["NICK"]
    del cod.s2scommands["BMASK"]
    del cod.s2scommands["MODE"]
    del cod.s2scommands["CHGHOST"]
    del cod.s2scommands["WHOIS"]
    del cod.s2scommands["JOIN"]
    del cod.s2scommands["SID"]
    del cod.s2scommands["ENCAP"]
    del cod.s2scommands["KILL"]
    del cod.s2scommands["STATS"]
    del cod.s2scommands["PING"]
    del cod.s2scommands["ERROR"]
    del cod.s2scommands["SQUIT"]
    del cod.s2scommands["TMODE"]

    cod.s2scommands["PRIVMSG"].remove(handlePRIVMSG)

def rehash():
    pass

def login(cod):
    """
    Sends the commands needed to authenticate to the remote IRC server.
    """

    cod.sendLine("PASS %s TS 6 :%s" % \
            (cod.config["uplink"]["pass"], cod.sid))
    cod.sendLine("CAPAB :QS EX IE KLN UNKLN ENCAP SERVICES EUID EOPMOD")
    cod.sendLine("SERVER %s 1 :%s" % \
            (cod.config["me"]["name"], cod.config["me"]["desc"]))

def burstClient(cod, client):
    """
    Some TS6-compatible IRC servers use different syntaxes for bursting clients,
    Thus, the protocol module needs to handle this.

    Takes in everything needed for a client to be bursted. Will auto-generate
    a UID if none is given.
    """

    cod.sendLine(client.burst())

def nullCommand(cod, line):
    """
    Useful for ignoring commands that should be implemented later
    """

    pass

def encapSU(cod, line):
    #<<< :00A ENCAP * SU 376100000 :ShadowNET
    if line.args[-1] == line.args[2]:
        cod.clients[line.args[2]].login = "*"
    else:
        cod.clients[line.args[2]].login = line.args[-1]

def handleEUID(cod, line):
    """
    Listens for EUID commands and adds information about remote clients
    accordingly.
    """
    # <<< :Home-server EUID Nick Hopcount TS umodes ident vhost realip UID realhost accountname :realname
    client = Client(line.args[0], line.args[7], line.args[2], line.args[3],
            line.args[4], line.args[5], line.args[6], line.args[9],
            line.args[-1])

    cod.clients[client.uid] = client
    cod.servers[client.uid[:3]].clients.append(client)

    cod.runHooks("newclient", [client])

def handleQUIT(cod, line):
    """
    Handles a client quitting from the network
    """

    client = cod.clients[line.source]
    cod.servers[client.uid[:3]].clients.remove(client)

    for chanuser in client.channels:
        try:
            chanuser.channel.del_member(chanuser.client)
        except:
            pass

    cod.pop_empty_channels()

    cod.clients.pop(line.source)

def handleSQUIT(cod, line):
    """
    Handles a server quitting from the network.
    """
    # <<< SQUIT 6LO :by shadowh511: shadowh511

    tokill = line.args[0]

    cod.servers.pop(tokill)

    for client in cod.clients:
        if client.sid == tokill:
            cod.clients.pop(client.uid)
    cod.pop_empty_channels()

def handleJOIN(cod, line):
    """
    Handles a raw S2S JOIN, this also handles JOIN 0.
    """

    if line.args[0] == "0":
        cod.clients[line.source].channnels = []
        cod.pop_empty_channels()
        return

    channel = cod.channels[line.args[1]]
    client = cod.clients[line.source]

    channel.add_member(client)

    cod.runHooks("join", [client, channel])

def handlePART(cod, line):
    """
    Handles a raw S2S PART, this removes a client from a channel.
    """
    channel = cod.channels[line.args[0]]

    try:
        channel.del_member(cod.clients[line.source])

        cod.pop_empty_channels()
    except:
        pass

    cod.runHooks("part", [cod.clients[line.source], channel])

def handleSJOIN(cod, line):
    """
    Handles an SJOIN line from the server to add clients to a channel. Relevant
    channel prefixes are passed into the ChanUser stub class for later handling.
    """

    # <<< :45X SJOIN 1385182842 #shadrips +nt :1AAAAAAA6 @00AAAAAA3 75XAAAADM 75XAAAACQ 69AAAAAAD 42JAAAAB4
    try:
        cod.channels[line.args[1]]
    except KeyError as e:
        cod.channels[line.args[1]] = Channel(line.args[1], line.args[0])
    finally:
        channel = cod.channels[line.args[1]]
        #Set channel modes
        for mode in line.args[2]:
            try:
                channel.add_prop_by_letter(True, mode)
            except KeyError:
                pass

        #Join users to channel
        uids = line.args[-1].split(" ")
        for uid in uids:
            #Extremely pro implementation

            prefix = uid[:-9]
            uid = uid[-9:]

            client = cod.clients[uid]

            channel.add_member(client, prefix)

            if cod.bursted:
                cod.runHooks("join", [client, channel])

def handleNICK(cod, line):
    """
    Handles a NICK line from the server. This changes a client's nickname.
    """

    cod.clients[line.source].nick = line.args[0]
    cod.clients[line.source].ts = line.args[-1]

def handleSID(cod, line):
    """
    Handles a SID line from the server. This gives information about a remote
    server link.
    """

    cod.servers[line.source] = Server(line.source, line.args[0], line.args[1],
            line.args[-1])

def handleBMASK(cod, line):
    """
    Handles a BMASK from the server. This communicates channel list-like modes,
    even though this protocol command was only made for ban modes.
    """

    channel = cod.channels[line.args[1]]
    ban_type = CHANMODES[0][line.args[2]]

    for mask in line.args[-1].split():
        ban = Ban(mask)
        channel.add_ban(ban_type, ban)

def handleMODE(cod, line):
    """
    A brilliant move was to make MODE both the client mode changing command
    and to make it the server to server command for USER MODES, while channel
    modes are handled on an S2S level by TMODE.
    """

    extparam = line.args[-1]

    if extparam.find("o") != -1:
        if extparam[0] == "+":
            cod.clients[line.source].isOper = True
        else:
            cod.clients[line.source].isOper = False

def handleTMODE(cod, line):
    """
    Handles channel mode changes
    """

    # Okay boys and girls, this is where it gets fun.
    # There are 5 types of channel modes.
    #
    # | Type | Param? | Description          |
    # |:---- |:------ |:-------------------- |
    # |  0   | Yes    | List-like modes      |
    # |  1   | Yes    | Key-like modes       |
    # |  2   | Yes    | argument modes       |
    # |  3   | No     | channel set modes    |
    # |  4   | Yes    | channel prefix modes |

    # :00AAAAAAY TMODE 1383760869 #niichan +yo 6LOAAAAKA 6LOAAAAKA

    modestring = line.args[2]
    params = line.args[3:]

    idx = 0
    paramcounter = 0
    set_mode = True

    channel = cod.channels[line.args[1]]

    for mode in modestring:
        if mode == "+":
            set_mode = True
        elif mode == "-":
            set_mode = False

        elif mode in CHANMODES[0]:
            #List-like mode
            if set_mode:
                ban = Ban(params[paramcounter], None, None)
                channel.add_ban(CHANMODES[0][mode], ban)
            else:
                channel.del_ban(CHANMODES[0][mode], params[paramcounter])

            paramcounter = paramcounter + 1

        elif mode in CHANMODES[1]:
            #Key
            paramcounter = paramcounter + 1

        elif mode in CHANMODES[2]:
            #Forwarding, limit and join throttle, not interested in these
            paramcounter += 1

        elif mode in CHANMODES[3]:
            channel.add_prop_by_letter(set_mode, mode)

            paramcounter += 1

        elif mode in CHANMODES[4]:
            # STATUS
            string = str("+" if set_mode else "-") + mode

            client = channel.clients[params[paramcounter]]
            client.add_prefix(string)
            paramcounter += 1

def handleCHGHOST(cod, line):
    """
    Changes the visible host of a client
    """

    cod.clients[line.args[0]].host = line.args[1]

def handleWHOIS(cod, line):
    """
    Replies to a WHOIS request by a client with relevant information about
    that service
    """

    service = line.args[0]

    client = cod.clients[service]

    cod.sendLine(":{0} 311 {1} {2} {3} {4} * :{5}".format(
        cod.sid, line.source, client.nick, client.user,
        client.host, client.gecos))
    cod.sendLine(":{0} 312 {1} {2} {3} :{4}".format(
        cod.sid, line.source, client.nick, cod.config["me"]["name"],
        cod.config["me"]["desc"]))
    cod.sendLine(":{0} 313 {1} {2} :is a Network Service".format(
        cod.sid, line.source, client.nick))
    cod.sendLine(":{0} 318 {1} {2} :End of /WHOIS list.".format(
        cod.sid, line.source, client.nick))

def handlePRIVMSG(cod, line):
    """
    Handle PRIVMSG
    """

    line.source = cod.clients[line.source]

    destination = line.args[0]

    if line.args[-1][0] == "\x01": # Ignore CTCP messages
        return

    if destination[0] == "#":
        cod.runHooks("chanmsg", [cod.channels[line.args[0]], line])
    else:
        cod.runHooks("privmsg", [cod.clients[line.args[0]], line])

    source = line.source
    line = line.args[-1]
    splitline = line.split()

    command = ""
    pm = True

    if line == []:
        return

    if destination[0] == "#":
        if destination not in cod.client.channels:
            return
        try:
            if line[0] == cod.config["me"]["prefix"]:
                command = splitline[0].upper()
                command = command[1:]
                pm = False
            else:
                possibilities = ["%s%s " % (cod.config["me"]["nick"], char) for char in [":", ","]]
                for mynick in possibilities:
                    mylen = len(mynick)
                    if line[:mylen] == mynick:
                        line = line[:mylen]
                        splitline = splitline[1:]
                        command = splitline[0].upper()
                        pm = False
                        break
        except IndexError as e:
            raise

    elif destination != cod.client.uid and pm:
        return

    else:
        destination = cod.clients[destination]
        command = splitline[0].upper()

    output = None

    if command in cod.opercommands:
        if source.isOper:
            for impl in cod.opercommands[command]:
                if pm:
                    output = impl(cod, line, splitline, source, source)
                else:
                    output = impl(cod, line, splitline, source, destination)
        else:
            cod.protocol.notice(cod.client, source, "Permission denied.")

    elif command in cod.botcommands:
        for impl in cod.botcommands[command]:
            if pm:
                output = impl(cod, line, splitline, source, source)
            else:
                output = impl(cod, line, splitline, source, destination)

    if output != None:
        if pm:
            cod.notice(source, output, destination)
        else:
            cod.reply(source, destination, output)

def handleERROR(cod, line):
    """
    Die on ERROR
    """

    cod.log(" ".join(line.args), "!!!")

    sys.exit(0)

def handleKILL(cod, line):
    """
    Reap off killed local clients and attempt to rejoin channels
    """

    if line.args[0] != cod.client.uid:
        cod.clients.pop(line.args[0])
        return

    cod.sendLine(cod.client.burst())

    for channel in cod.client.channels:
        cod.join(channel)

    cod.servicesLog("KILL'd by %s " % cod.clients[source].nick)

def handleSTATS(cod, line):
    """
    Reply to remote STATS commands
    """

    if line.args[0] == "v":
        cod.notice(line.source, "Cod version %s" % cod.version)

    elif line.args[0] == "c":
        cod.notice(line.source, "%d clients in ram" % len(cod.clients))

    elif line.args[0] == "C":
        cod.notice(line.source, "%d channels in ram" % len(cod.channels))

    elif line.args[0] == "m":
        cod.notice(line.source, "%d modules loaded" % len(cod.modules))

    elif line.args[0] == "M":
        cod.notice(line.source, "%d protocol commands loaded" % len(cod.s2scommands))
        cod.notice(line.source, "%d bot commands loaded" % len(cod.botcommands))
    elif line.args[0] == "h":
        cod.notice(line.source, "%d types of hooks loaded" % len(cod.hooks))

        amount = 0

        for name, hooks in cod.hooks.iteritems():
            amount += len(hooks)

        cod.notice(line.source, "%d hooks loaded" % amount)
    else:
        cod.notice(line.source, "Stats commands: [v]ersion, [c]lients, [C]hannels, [m]odules, co[M]mands, [h]ooks")

    cod.notice(line.source, "End of /STATS report")

def handlePING(cod, line):
    """
    Pongs remote servers to end bursting
    """

    if not cod.bursted:
        #Join staff and snoop channels
        cod.join(cod.config["etc"]["staffchan"])
        cod.join(cod.config["etc"]["snoopchan"])
        cod.privmsg("NickServ", "IDENTIFY %s" % cod.config["me"]["servicespass"])

        #Load admin module
        cod.loadmod("admin") #Required to be hard-coded
        cod.loadmod("help")

        cod.bursted = True

    cod.sendLine(":%s PONG %s :%s" %
            (cod.sid, cod.config["me"]["name"],
                line.args[-1]))

def handleSID(cod, line):
    cod.servers[line.args[2]] = Server(line.args[2], line.args[0], line.args[1])
