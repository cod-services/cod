"""
<license header>
"""

NAME="Sendfile"
DESC="allows you to send people files"

from utils import *

def initModule(cod):
    cod.botcommands["SENDFILE"] = [sendfileCMD]

def destroyModule(cod):
    del cod.botcommands["SENDFILE"]

def rehash():
    pass

def sendfileCMD(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.client, cod.clients[source]):
        return

    if len(splitline) < 3:
        cod.reply(source, destination, "SENDFILE <target> <path>")
        return

    with open("etc/sendfile/" + splitline[2], "r") as f:
        for line in f:
            cod.privmsg(splitline[1], line)

    cod.servicesLog("%s: SENDFILE %s: %s" %
            (cod.clients[source].nick, splitline[1], splitline[2]))

