NAME="Say command"
DESC="Sends arbitrary text to a channel"

from utils import *

def initModule(cod):
    cod.botcommands["SAY"] = [say]

def destroyModule(cod):
    del cod.botcommands["SAY"]

def say(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.client, cod.clients[source]):
        return

    cod.privmsg(splitline[1], " ".join(splitline[2:]))

    cod.servicesLog("SAY: %s to %s" %
            (cod.clients[source].nick, splitline[1]))

