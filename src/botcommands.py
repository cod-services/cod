from structures import *
import rblwatch
import mpd
from random import randint

#Initialization for military operation name generator

prefix = []
suffix = []

def failIfNotOper(cod, client):
    if not client.isOper:
        cod.notice(client.uid, "Insufficient permissions")
        return True
    else:
        return False

def commandTEST(cod, line, splitline, source, destination):
    if destination == source:
        #In a PM, the destination will anways be the source
        cod.notice(destination, "Hello!")
    else:
        cod.privmsg(destination, "Hello!")

def commandJOIN(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    if splitline[1][0] == "#":
        channel = splitline[1]

        cod.join(channel, False)

        client = cod.clients[source]
        cod.servicesLog("JOIN %s: %s" % (channel, client.nick))
        cod.notice(source, "I have joined to %s", channel)

    else:
        cod.notice(source, "USAGE: JOIN #channel")

def commandRBL(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    if destination != cod.config["etc"]["snoopchan"]:
        cod.notice(source, "Command may not be used outside %s" % cod.config["etc"]["snoopchan"])
        return

    search = None
    target = splitline[1]

    if splitline[1].find(".") == -1:
        #If we don't have an IP address, we have a nick of a client
        mark = None

        for client in cod.clients:
            if cod.clients[client].nick == target:
                mark = client
                break

        if mark == None:
            cod.notice(source, "%s is not on IRC" % target)

        mark = cod.clients[mark]

        if mark.ip == "0":
            cod.notice(source, "Target is a network service")
            return

        cod.servicesLog("RBL: %s: %s" % (target, cod.clients[source].nick))

        search = rblwatch.RBLSearch(cod, mark.ip)

    else:
        cod.servicesLog("RBL: %s: %s" % (target, cod.clients[source].nick))

        search = rblwatch.RBLSearch(cod, target)

    search.print_results()

def commandMPD(cod, line, splitline, source, destination):
    if not cod.config["mpd"]["enable"]:
        return

    if splitline[1].upper() == "FIND":
        query = " ".join(splitline[2:])

        cod.privmsg(destination, "Searching for %s" % query)

        results = cod.mpd.find("any", query)

        client = cod.clients[source]

        for result in results:
            cod.privmsg(destination, "%s: %s -- %s" %
                    (client.nick, result["artist"], result["title"]))

    elif splitline[1].upper() == "STATUS":
        cur = cod.mpd.currentsong()

        cod.privmsg(destination, "%s -- %s -- %4.2f%%" %
                (cur["artist"], cur["title"], float(cur["pos"])/float(cur["time"])))

def commandREHASH(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    cod.rehash()

    client = cod.clients[source]
    cod.servicesLog("REHASH: %s" % client.nick)

def commandOPNAMEinit(cod, line, splitline, source, destination):
    global prefix, suffix

    if not prefix == []:
        return

    #Prepare lists
    prefixfile = open(cod.config["etc"]["prefixfile"], 'r')
    suffixfile = open(cod.config["etc"]["suffixfile"], 'r')
    prefix = prefixfile.readlines()
    suffix = suffixfile.readlines()
    prefixfile.close()
    suffixfile.close()

    #Strip the lists
    for junk in range(len(prefix)-1, -1, -1):
        prefix[junk] = prefix[junk].strip()
        if len(prefix[junk]) == 0:
            prefix.pop(junk)
    for junk in range(len(suffix)-1, -1, -1):
        suffix[junk] = suffix[junk].strip()
        if len(suffix[junk]) == 0:
            suffix.pop(junk)

def commandOPNAME(cod, line, splitline, source, destination):
    #Format string
    if (randint(0,9)==0):
        phrase = "OPERATION %s %s %s" % \
            (prefix[randint(0, len(prefix) - 1)],
                prefix[randint(0, len(prefix) - 1)],
                suffix[randint(0, len(suffix) - 1)]) #3
    else:
        phrase = "OPERATION %s %s" % \
            (prefix[randint(0, len(prefix) - 1)],
                suffix[randint(0, len(suffix) - 1)]) #2

    cod.privmsg(destination, phrase.upper())

def commandDIE(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    cod.servicesLog("DIE: %s" % cod.clients[source].nick)

    cod.sendLine(cod.client.quit())

    cod.sendLine("SQUIT")

