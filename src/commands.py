from structures import *

def nullCommand(cod, line, splitline, source):
    pass

def handleEUID(cod, line, splitline, source):
    client = Client(splitline[2], splitline[9], splitline[4], splitline[5], splitline[6], splitline[7], splitline[8], splitline[11], splitline[12][1:])

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
            cod.clients[sourcd].isOper = False

CHANMODES=["eIbq", "k" ,"flj" ,"CDEFGJKLMOPQTcdgimnpstz", "yaohv"]

def handleTMODE(cod, line, splitline, source):
    modechange = " ".join(splitline[4:])

    """
    0 = Mode that adds or removes a nick or address to a list. Always has a parameter.
    1 = Mode that changes a setting and always has a parameter.
    2 = Mode that changes a setting and only has a parameter when set.
    3 = Mode that changes a setting and never has a parameter.
    4 = Mode that indicates a channel prefix being added or removed.
    """

    plus = True
    index = 1
    channel = cod.channels[splitline[3]]

    for mode in splitline[4]:
        if mode == "+":
            plus = True

        elif mode == "-":
            plus = False

        elif mode in CHANMODES[0]:
            #List-like mode
            subMode(cod, source, plus, " ".join([mode, modechange[index]]), channel)
            index += 1

        elif mode in CHANMODES[1]:
            #mode change has a parameter
            subMode(cod, source, plus, " ".join([mode, modechange[index]]), channel)
            index += 1

        elif mode in CHANMODES[2]:
            #mode change has a parameter when set
            if plus:
                subMode(cod, source, plus, " ".join([mode, modechange[index]]), channel)
                index += 1
            else:
                subMode(cod, source, plus, mode, channel)

        elif mode in CHANMODES[3]:
            #Normal channel mode
            subMode(cod, source, plus, mode, channel)

        elif mode in CHANMODES[4]:
            #Prefix mode
            subMode(cod, source, plus, " ".join([mode, modechange[index]]), channel)
            index += 1

def subMode(cod, source, plus, mode, channel):
    pass

def handleCHGHOST(cod, line, splitline, source):
    cod.clients[splitline[2]].host = splitline[3]

def handleWHOIS(cod, line, splitline, source):
    service = splitline[2]

    client = cod.clients[service]

    cod.sendLine(":{0} 311 {1} {2} {3} {4} * :{5}".format(
        cod.config["uplink"]["sid"], source, cod.config["me"]["nick"], cod.config["me"]["user"],
                cod.config["me"]["host"], cod.config["me"]["desc"]))
    cod.sendLine(":{0} 312 {1} {2} {3} :{4}".format(
        cod.config["uplink"]["sid"], source, cod.config["me"]["nick"], cod.config["me"]["name"],
        cod.config["me"]["desc"]))
    cod.sendLine(":{0} 313 {1} {2} :is a Network Service".format(
        cod.config["uplink"]["sid"], source, cod.config["me"]["nick"]))
    cod.sendLine(":{0} 318 {1} {2} End of /WHOIS list.".format(
        cod.config["uplink"]["sid"], source, cod.config["me"]["nick"]))

def handleKILL(cod, line, splitline, source):
    victim = cod.clients[splitline[2]]
    killer = cod.clients[source]

    if killer.nick != "NickServ":
        cod.servicesLog("%s: KILL %s %s" % (killer.nick, victim.nick, splitline[4]))

