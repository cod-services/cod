from structures import *
from botcommands import *

commands = {}

def relayHostServToOpers(cod, line, splitline, source):
    if splitline[2] == "#services":
        if cod.clients[source].nick == "HostServ":
            cod.sendLine(cod.client.privmsg("#opers", "HostServ" + " ".join (splitline[3:])))

def handlePRIVMSG(cod, line, splitline, source):
    pass

commands["OPER"] = commandOPER

