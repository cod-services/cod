from utils import *
from structures import *

def initModule(cod):
    cod.botcommands["JOIN"] = [commandJOIN]
    cod.botcommands["REHASH"] = [commandREHASH]
    cod.botcommands["DIE"] = [commandDIE]
    cod.botcommands["MODLOAD"] = [commandMODLOAD]
    cod.botcommands["MODUNLOAD"] = [commandMODUNLOAD]

def destroyModule(cod):
    del cod.botcommands["JOIN"]
    del cod.botcommands["REHASH"]
    del cod.botcommands["DIE"]
    del cod.botcommands["MODLOAD"]
    del cod.botcommands["MODUNLOAD"]

def commandJOIN(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    if splitline[1][0] == "#":
        channel = splitline[1]

        cod.join(channel, False)

        client = cod.clients[source]
        cod.servicesLog("JOIN %s: %s" % (channel, client.nick))
        cod.reply(source, destination, "I have joined to %s" % channel)

    else:
        cod.reply(source, destination, "USAGE: JOIN #channel")

def commandREHASH(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    cod.rehash()

    client = cod.clients[source]
    cod.servicesLog("REHASH: %s" % client.nick)

def commandDIE(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    cod.servicesLog("DIE: %s" % cod.clients[source].nick)

    cod.sendLine(cod.client.quit())

    cod.sendLine("SQUIT")

def commandMODLOAD(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    target = splitline[1].lower()

    if target in cod.modules:
        cod.notice(source, "Module %s is loaded" % target)
        return

    try:
        cod.loadmod(target)
    except ImportError as e:
        cod.reply(source, destination, "Module %s failed load: %s" % (target, e))

    cod.servicesLog("MODLOAD:%s: %s" % (target, cod.clients[source].nick))

def commandMODUNLOAD(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    target = splitline[1].lower()

    if target not in cod.modules:
        cod.notice(source, "Module %s is not loaded" % target)
        return

    try:
        cod.unloadmod(target)
    except Exception as e:
        cod.reply(source, destination, "Module %s failed unload: %s" % (target, e))

    cod.servicesLog("MODUNLOAD:%s: %s" % (target, cod.clients[source].nick))

