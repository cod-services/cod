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

from utils import *
from structures import *
import traceback
import sys
import subprocess

NAME="Admin"
DESC="Administrative commands"

global motd

motd = []

def initModule(cod):
    global motd

    cod.addBotCommand("JOIN", commandJOIN, True)
    cod.addBotCommand("PART", commandPART, True)
    cod.addBotCommand("REHASH", commandREHASH, True)
    cod.addBotCommand("DIE", commandDIE, True)
    cod.addBotCommand("MODLOAD", commandMODLOAD, True)
    cod.addBotCommand("MODLIST", commandMODLIST, True)
    cod.addBotCommand("MODUNLOAD", commandMODUNLOAD, True)
    cod.addBotCommand("LISTCHANS", commandLISTCHANS, True)
    cod.addBotCommand("VERSION", commandVERSION, True)
    cod.addBotCommand("UPGRADE", commandUPGRADE, True)
    cod.addBotCommand("UPDATE", commandUPGRADE, True)

    cod.s2scommands["ENCAP"].append(logREHASH)
    cod.s2scommands["MOTD"] = [handleMOTD]

    initDBTable(cod, "Moduleautoload", "Id INTEGER PRIMARY KEY, Name TEXT")
    initDBTable(cod, "Joins", "Id INTEGER PRIMARY KEY, Name TEXT")


    rows = lookupDB(cod, "Moduleautoload")

    if rows != []:
        for row in rows:
            try:
                cod.loadmod(row[1])
            except AttributeError:
                pass

    rows = lookupDB(cod, "Joins")

    if rows == []:
        return

    for row in rows:
        cod.join(row[1])

    with open(cod.config["me"]["motd"], "r") as fin:
        cod.log("reading MOTD from %s" % cod.config["me"]["motd"], "===")
        for line in fin.readlines():
            motd.append(line.strip())

def destroyModule(cod):
    global motd

    cod.delBotCommand("JOIN")
    cod.delBotCommand("PART")
    cod.delBotCommand("REHASH")
    cod.delBotCommand("DIE")
    cod.delBotCommand("MODLOAD")
    cod.delBotCommand("MODUNLOAD")
    cod.delBotCommand("LISTCHANS")
    cod.delBotCommand("VERSION")
    cod.delBotCommand("UPGRADE")
    cod.delBotCommand("UPDATE")

    idx = cod.s2scommands["ENCAP"].index(logREHASH)
    cod.s2scommands.pop(idx)

    del cod.s2scommands["MOTD"]
    del motd

def rehash():
    pass

def commandJOIN(cod, line, splitline, source, destination):
    "Makes Cod join a channel. This does not check bans."

    if splitline[1][0] == "#":
        channel = splitline[1]

        if splitline[1] not in cod.channels:
            cod.notice(source, "I don't know about %s" % channel)
            return

        cod.join(channel)

        client = source
        cod.servicesLog("JOIN %s: %s" % (channel, client.nick))
        cod.notice(source, "I have joined %s" % channel)

        addtoDB(cod, "INSERT INTO Joins(Name) VALUES ('%s');" % channel)

    else:
        cod.notice(source, "USAGE: JOIN #channel")

def commandPART(cod, line, splitline, source, destination):
    "Makes Cod leave a cahnnel."

    if splitline[1][0] == "#":
        channel = splitline[1]

        client = source
        cod.servicesLog("PART %s: %s" % (channel, client.nick))
        cod.notice(source, "I have left %s" % channel)

        cod.part(channel, "Requested by %s" % client.nick)

        deletefromDB(cod, "DELETE FROM Joins WHERE Name = \"%s\"" % channel)

    else:
        cod.notice(source, "USAGE: PART #channel")

def commandREHASH(cod, line, splitline, source, destination):
    "Rehashes Cod's configuration file from the disk."

    cod.rehash()

    client = source
    cod.servicesLog("REHASH: %s" % client.nick)

def commandDIE(cod, line, splitline, source, destination):
    "Kills off Cod"

    cod.servicesLog("DIE: %s" % source.nick)

    raise KeyboardInterrupt()

def commandMODLIST(cod, line, splitline, source, destination):
    "Sends information about currently running modules to the oper requesting it."

    for module in cod.modules:
        try:
            cod.notice(source, "%s: %s" % (module, cod.modules[module].DESC))
        except:
            cod.servicesLog("%s does not have a DESC! BUG!" % module)

    cod.notice(source, "End of module list, %d modules loaded" % len(cod.modules))

def commandMODLOAD(cod, line, splitline, source, destination):
    "Makes Cod try to load a module."

    if len(splitline) < 2:
        cod.notice(source, "Need name of module")
        return

    target = splitline[1].lower()

    if target in cod.modules:
        cod.notice(source, "Module %s is loaded" % target)
        return

    cod.rehash()

    try:
        cod.loadmod(target)
    except Exception as e:
        cod.reply(source, destination, "Module %s failed load: %s" % (target, e))
        traceback.print_exc(file=sys.stdout)
        return

    addtoDB(cod, "INSERT INTO Moduleautoload(Name) VALUES ('%s');" % target)

    cod.servicesLog("MODLOAD:%s: %s" % (target, source.nick))

    cod.reply(source, destination, "%s loaded." % target)

def commandMODUNLOAD(cod, line, splitline, source, destination):
    "Makes Cod unload a module."

    if len(splitline) < 2:
        cod.notice(source, "Need name of module")
        return

    target = splitline[1].lower()

    if target not in cod.modules:
        cod.notice(source, "Module %s is not loaded" % target)
        return

    cod.rehash()

    try:
        cod.unloadmod(target)
    except Exception as e:
        cod.reply(source, destination, "Module %s failed unload: %s" % (target, e))
        return

    deletefromDB(cod, "DELETE FROM Moduleautoload WHERE Name = \"%s\";" % target)

    cod.servicesLog("MODUNLOAD:%s: %s" % (target, source.nick))

    cod.reply(source, destination, "%s unloaded." % target)

def commandLISTCHANS(cod, line, splitline, source, destination):
    "Lists all the channels Cod is set to autojoin."

    rows = lookupDB(cod, "Joins")

    if rows == []:
        cod.notice(source, "No channel joins in database")
        return

    for row in rows:
        cod.notice(source, "AUTOJOIN: %d - %s" % (row[0], row[1]))

    cod.notice(source, "End of channel list")

def logREHASH(cod, line):
    if line.args[1] == "REHASH":
        cod.rehash()

        cod.servicesLog("REHASH: %s" % cod.clients[line.source].nick)

def handleMOTD(cod, line):
    global motd

    for mline in motd:
        cod.notice(line.source, "MOTD: %s" % mline)

    cod.notice(line.source, "End of /MOTD")

def commandVERSION(cod, line, splitline, source, destination):
    "Shows Cod's version information."

    cod.notice(source, "Cod version %s" % cod.version)

def commandUPGRADE(cod, line, splitline, source, destination):
    "Updrace Cod's code on the disk without reloading anything."

    p = subprocess.Popen(["git","pull"], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    output, stderrdata = p.communicate()

    output = output.split("\n")

    for line in output:
        cod.reply(source, destination, (line.strip()))

    cod.servicesLog("%s: UPGRADE" % source.nick)

