from structures import *
import rblwatch
import mpd

def failIfNotOper(cod, client):
    if not client.isOper:
        cod.notice(client.uid, "Insufficient permissions")
        return True
    else:
        return False

def commandTEST(cod, line, splitline, source, destination):
    cod.privmsg(destination, "Hello!")

def commandJOIN(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    if splitline[1][0] == "#":
        channel = splitline[1]

        try:
            if splitline[2] == "@":
                cod.join(channel)
                channel = "@" + channel

        except IndexError as e:
            cod.join(channel, False)

        client = cod.clients[source]
        cod.servicesLog("%s: JOIN %s" % (client.nick, channel))

    else:
        cod.notice(source, "USAGE: JOIN #channel <@ or nothing>")

def commandRBL(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    if destination != "#services":
        cod.notice(source, "Command may not be used outside #services")
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

        cod.servicesLog("%s: RBL: %s" % (cod.clients[source].nick, target))

        search = rblwatch.RBLSearch(cod, mark.ip)

    else:
        cod.servicesLog("%s: RBL: %s" % (cod.clients[source].nick, target))

        search = rblwatch.RBLSearch(cod, target)

    search.print_results()

def commandMPD(cod, line, splitline, source, destination):
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
