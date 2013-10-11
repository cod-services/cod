from utils import *
from structures import *

import rblwatch

def initModule(cod):
    cod.botcommands["RBL"] = [commandRBL]

def destroyModule(cod):
    del cod.botcommands["RBL"]

def commandRBL(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    search = None
    target = splitline[1]

    if splitline[1].find(".") == -1:
        #If we don't have an IP address, we have a nick of a client
        mark = None

        client = cod.findClientByNick(target)

        if client.ip == "0":
            reply(cod, source, destination, "Error: target %s is a network service" % client.nick)
            return

        target = client.ip

    cod.servicesLog("RBL: %s: %s" % (target, cod.clients[source].nick))

    search = rblwatch.RBLSearch(cod, target)

    search.print_results()

