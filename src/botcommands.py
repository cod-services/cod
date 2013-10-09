from structures import *
import rblwatch

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

    if destination != "#services" or destination[0] != "#":
        cod.notice(source, "Command may not be used outside #services or PM")
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

        cod.servicesLog("%s: RBL: %s" % (cod.clients[source].nick, target))

        mark = cod.clients[mark]

        search = rblwatch.RBLSearch(cod, mark.ip)

    else:
        search = rblwatch.RBLSearch(cod, target)

    search.print_results()


