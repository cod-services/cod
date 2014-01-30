"""
Copyright (c) 2013, Sam Dodrill
All rights reserved.

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

    1. The origin of this software must not be misrepresented; you must not
    claim that you wrote the original software. If you use this software
    in a product, an acknowledgment in the product documentation would be
    appreciated but is not required.

    2. Altered source versions must be plainly marked as such, and must not be
    misrepresented as being the original software.

    3. This notice may not be removed or altered from any source
    distribution.
"""

NAME="Orbital Friendship Cannon"
DESC="Stress tester"

from utils import *
from structures import *
from random import choice
from random import randint

global prefix, suffix, slaves

prefix = []
suffix = []
slaves = []

def initModule(cod):
    global prefix, suffix, slaves

    prefix = []
    suffix = []
    slaves = []

    #Initialize Database table
    initDBTable(cod, "OFCStats", "Id INTEGER PRIMARY KEY, Clients INTEGER")

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
    cod.addBotCommand("OFC", ofc, True)

def destroyModule(cod):
    global prefix, suffix, slaves

    for slave in slaves:
        cod.sendLine(slave.quit())
        try:
            del cod.clients[slave.uid]
        except:
            continue

    del slaves
    del prefix
    del suffix

    cod.delBotCommand("OFC")

def rehash():
    pass

def help(cod, source):
    cod.notice(source, "Valid commands are:")
    cod.notice(source, "OFC CLIENTJOIN #channel")
    cod.notice(source, " - Joins a lot of clients to #channel")
    cod.notice(source, "OFC SPAM #channel")
    cod.notice(source, " - Has each client spam #channel")
    cod.notice(source, "OFC KILL CLIENTS")
    cod.notice(source, " - Kills off the bots")
    cod.notice(source, "OFC STATS LIST")
    cod.notice(source, " - Displays statistics about Orbital Friendship Cannon runs")

def ofc(cod, line, splitline, source, destination):
    global slaves

    if len(splitline) < 2:
        help(cod, source)
        return

    if splitline[1].upper() == "STATS":
        stats(cod, source)


    if len(splitline) < 3:
        help(cod, source)
        return

    if splitline[1].upper() == "CLIENTJOIN":
        joinclients(cod, splitline[2], source)
    elif splitline[1].upper() == "SPAM":
        decimate(cod, source, splitline[2])
    elif splitline[1].upper() == "KILL":
        depart(cod, source)
    else:
        help(cod, source)

def joinclients(cod, channel, source):
    global slaves, nicks

    number = 1500

    for n in range(number):
        user = "~lel~"

        uid = cod.getUID()

        slave = makeClient(uid, user, uid, "CareFriend", uid)
        slaves.append(slave)
        cod.burstClient(cod, slave)
        cod.join(channel, slave)

        cod.clients[slave.uid] = slave

    cod.notice(source, "%d clients joined to %s" % (number, channel))

    cod.servicesLog("OFC:CLIENTJOIN: %d clients to %s requested by %s" %
            (number, channel, source.nick))

def decimate(cod, source, channel):
    global slaves

    for slave in slaves:
        phrase = "%s %s %s" % \
                (prefix[randint(0, len(prefix) - 1)],
                        prefix[randint(0, len(prefix) - 1)],
                        suffix[randint(0, len(suffix) - 1)])

        cod.sendLine(slave.privmsg(channel, "OPERATION %s" % phrase.upper()))

    num = len(slaves)

    addtoDB(cod, "INSERT INTO OFCStats(Clients) VALUES ('%d');" % num)

    cod.servicesLog("OFC:DECIMATE: %d messages to %s requested by %s" %
            (len(slaves), channel, cod.clients[source].nick))

def depart(cod, source):
    global slaves

    num = len(slaves)

    for slave in slaves:
        cod.sendLine(slave.quit())

        try:
            del cod.clients[slave.uid]
        except:
            continue

    cod.notice(source, "%d slaves deleted" % num)

    cod.servicesLog("OFC:DEPART: requested by %s" % source.nick)

def stats(cod, source):
    rows = lookupDB(cod, "OFCStats")

    if rows == []:
        cod.notice(source, "The cannon has not been run yet. Please run the cannon and try again.")
        return

    maxclients = 0
    avgclients = 0
    totalclients = 0

    for row in rows:
        if row[1] > maxclients:
            maxclients = row[1]

        totalclients = totalclients + row[1]

    avgclients = float(totalclients)/len(rows)

    cod.notice(source, "STATS for Orbital Friendship Cannon:")
    cod.notice(source, " - %d runs, average of %4.2f clients per run" % (len(rows), avgclients))
    cod.notice(source, " - Maximum of %d clients in a single run" % maxclients)
    cod.notice(source, "END OF STATS")

