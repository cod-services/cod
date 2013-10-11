"""
Orbital Friendship cannon
"""

from utils import *
from structures import *
from random import choice
from random import randint

global prefix, suffix, slaves

prefix = []
suffix = []
slaves = []

def initModule(cod):
    global prefix, suffix

    #Read prefix and suffix lines in
    with open(cod.config["etc"]["prefixfile"], 'r') as prefixfile:
        cod.log("Reading in prefixes from %s" % cod.config["etc"]["prefixfile"], "===")
        prefix = prefixfile.readlines()
    with open(cod.config["etc"]["suffixfile"], 'r') as suffixfile:
        cod.log("Reading in suffixes from %s" % cod.config["etc"]["suffixfile"], "===")
        suffix = suffixfile.readlines()

    #Strip lines and prune junk lines
    for ix in [prefix, suffix]:
        for junk in range(len(ix)-1, -1, -1):
            ix[junk] = ix[junk].strip()

    #Register bot commands
    cod.botcommands["OFC"] = [ofc]

def destroyModule(cod):
    global prefix, suffix, slaves

    for slave in slaves:
        cod.sendLine(slave.quit())

    del slaves
    del prefix
    del suffix

    del cod.botcommands["OFC"]

def help(cod, source):
    cod.notice(source, "Valid commands are:")
    cod.notice(source, "OFC CLIENTJOIN #channel")
    cod.notice(source, " - Joins 500 clients to #channel")
    cod.notice(source, "OFC SPAM #channel")
    cod.notice(source, " - Has each client spam #channel")

def ofc(cod, line, splitline, source, destination):
    global slaves

    if failIfNotOper(cod, cod.clients[source]):
        return

    if len(splitline) < 3:
        help(cod, source)
        return

    if splitline[1].upper() == "CLIENTJOIN":
        joinclients(cod, splitline[2])
    if splitline[1].upper() == "SPAM":
        decimate(cod, splitline[2])

def joinclients(cod, channel):
    global slaves

    for n in range(500):
        nick = prefix[randint(0, len(prefix) - 1)].upper() + prefix[randint(0, len(prefix) - 1)].upper()
        user = "~lel~"
        host = "%s.%s.%s" %(prefix[randint(0, len(prefix) - 1)].upper(),
            prefix[randint(0, len(prefix) - 1)].upper(),
            suffix[randint(0, len(suffix) - 1)].upper())

        #Strip characters that are invalid in nicknames
        for char in [" ", "-", "&", "(", ")", ".", ",", "/", "'"]:
            nick = "".join(nick.split(char))

        #Truncate nick to normal maximum length
        nick = nick[:20]

        host = ".".join(host.split())

        if len(nick) < 6:
            nick = nick + nick

        slave = makeService(nick, user, host, "CareFriend", cod.config["uplink"]["sid"] + nick[:6])
        slaves.append(slave)
        cod.sendLine(slave.burst())
        cod.sendLine(slave.join(cod.channels[channel]))

def decimate(cod, channel):
    global slaves

    for slave in slaves:
        phrase = "%s %s %s" % \
                (prefix[randint(0, len(prefix) - 1)],
                        prefix[randint(0, len(prefix) - 1)],
                        suffix[randint(0, len(suffix) - 1)])

        cod.sendLine(slave.privmsg(channel, "OPERATION %s" % phrase.upper()))

