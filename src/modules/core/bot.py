from structures import *
from botcommands import *

def initModule(cod):
    if cod.config["etc"]["relayhostserv"]:
        cod.s2scommands["PRIVMSG"].append(relayHostServToOpers)

    cod.s2scommands["PRIVMSG"].append(prettyPrintMessages)

    cod.botcommands["TEST"] = [commandTEST]
    cod.botcommands["JOIN"] = [commandJOIN]
    cod.botcommands["RBL"] = [commandRBL]
    cod.botcommands["MPD"] = [commandMPD]
    cod.botcommands["OPNAME"] = [commandOPNAMEinit, commandOPNAME]
    cod.botcommands["REHASH"] = [commandREHASH]
    cod.botcommands["DIE"] = [commandDIE]

def destroyModule(cod):
    del cod.botcommands["TEST"]
    del cod.botcommands["JOIN"]
    del cod.botcommands["RBL"]
    del cod.botcommands["MPD"]
    del cod.botcommands["OPNAME"]
    del cod.botcommands["REHASH"]
    del cod.botcommands["DIE"]

def relayHostServToOpers(cod, line, splitline, source):
    if splitline[2] == "#services":
        if cod.clients[source].nick == "HostServ":
            cod.sendLine(cod.client.privmsg(cod.config["etc"]["staffchan"],
                "HostServ: " + " ".join (splitline[3:])[1:]))

def prettyPrintMessages(cod, line, splitline, source):
    if not cod.config["etc"]["production"]:
        client = cod.clients[source]

        print "{0}: <{1}> {2}".format(splitline[2], client.nick, " ".join (splitline[3:])[1:])

