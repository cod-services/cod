from structures import *
from botcommands import *

def initModule(cod):
    if cod.config["etc"]["relayhostserv"]:
        cod.s2scommands["PRIVMSG"].append(relayHostServToOpers)

    cod.s2scommands["PRIVMSG"].append(prettyPrintMessages)

def destroyModule(cod):
    if cod.config["etc"]["relayhostserv"]:
        cod.s2scommands.pop(relayHostServToOpers)

    cod.s2scommands.pop(prettyPrintMessages)

def relayHostServToOpers(cod, line, splitline, source):
    if splitline[2] == "#services":
        if cod.clients[source].nick == "HostServ":
            cod.sendLine(cod.client.privmsg(cod.config["etc"]["staffchan"],
                "HostServ: " + " ".join (splitline[3:])[1:]))

def prettyPrintMessages(cod, line, splitline, source):
    if not cod.config["etc"]["production"]:
        client = cod.clients[source]

        print "{0}: <{1}> {2}".format(splitline[2], client.nick, " ".join (splitline[3:])[1:])

