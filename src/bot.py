from structures import *
from botcommands import *

commands = {}

def relayHostServToOpers(cod, line, splitline, source):
    if splitline[2] == "#services":
        if cod.clients[source].nick == "HostServ":
            cod.sendLine(cod.client.privmsg("#opers", "HostServ: " + " ".join (splitline[3:])[1:]))

def prettyPrintMessages(cod, line, splitline, source):
    client = cod.clients[source]
    print "{0}: <{1}> {2}".format(splitline[2], client.nick, " ".join (splitline[3:])[1:])

def handlePRIVMSG(cod, line, splitline, source):
    destination = splitline[2]
    line = ":".join(line.split(":")[2:])
    splitline = line.split()

    command = splitline[0].upper()

    try:
        for impl in commands[command]:
            impl(cod, line, splitline, source, destination)
    except KeyError as e:
        pass

commands["TEST"] = [commandTEST]

