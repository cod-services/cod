from structures import *

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

