from utils import *
from structures import *

NAME="Admin"
DESC="Administrative commands"

global motd

motd = []

def initModule(cod):
    global motd

    cod.botcommands["JOIN"] = [commandJOIN]
    cod.botcommands["PART"] = [commandPART]
    cod.botcommands["REHASH"] = [commandREHASH]
    cod.botcommands["DIE"] = [commandDIE]
    cod.botcommands["MODLOAD"] = [commandMODLOAD]
    cod.botcommands["MODLIST"] = [commandMODLIST]
    cod.botcommands["MODUNLOAD"] = [commandMODUNLOAD]
    cod.botcommands["LISTCHANS"] = [commandLISTCHANS]
    cod.botcommands["VERSION"] = [commandVERSION]

    cod.s2scommands["ENCAP"] = [logREHASH]
    cod.s2scommands["MOTD"] = [handleMOTD]

    initDBTable(cod, "Joins", "Id INTEGER PRIMARY KEY, Name TEXT")

    cur = cod.db.cursor()
    cur.execute("SELECT * FROM Joins;")

    rows = cur.fetchall()

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

    del cod.botcommands["JOIN"]
    del cod.botcommands["PART"]
    del cod.botcommands["REHASH"]
    del cod.botcommands["DIE"]
    del cod.botcommands["MODLOAD"]
    del cod.botcommands["MODUNLOAD"]
    del cod.botcommands["LISTCHANS"]
    del cod.botcommands["VERSION"]

    idx = cod.s2scommands["ENCAP"].index(logREHASH)
    cod.s2scommands.pop(idx)

    del cod.s2scommands["MOTD"]
    del motd

def commandJOIN(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.client, cod.clients[source]):
        return

    if splitline[1][0] == "#":
        channel = splitline[1]

        cod.join(channel, False)

        client = cod.clients[source]
        cod.servicesLog("JOIN %s: %s" % (channel, client.nick))
        cod.notice(source, "I have joined %s" % channel)

        cur = cod.db.cursor()

        cur.execute("INSERT INTO Joins(Name) VALUES ('%s');" % channel)

        cod.db.commit()

    else:
        cod.notice(source, "USAGE: JOIN #channel")

def commandPART(cod, line, splitline, source, destination):
     if failIfNotOper(cod, cod.client, cod.clients[source]):
         return

     if splitline[1][0] == "#":
        channel = splitline[1]

        client = cod.clients[source]
        cod.servicesLog("PART %s: %s" % (channel, client.nick))
        cod.notice(source, "I have left %s" % channel)

        cod.part(channel, "Requested by %s" % client.nick)

        cur = cod.db.cursor()
        cur.execute("DELETE FROM Joins WHERE Name = \"%s\"" % channel)

        cod.db.commit()

     else:
        cod.notice(source, "USAGE: PART #channel")

def commandREHASH(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.client, cod.clients[source]):
        return

    cod.rehash()

    client = cod.clients[source]
    cod.servicesLog("REHASH: %s" % client.nick)

def commandDIE(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.client, cod.clients[source]):
        return

    cod.servicesLog("DIE: %s" % cod.clients[source].nick)

    cod.db.close()

    cod.sendLine(cod.client.quit())

    cod.sendLine("SQUIT")

def commandMODLIST(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.client, cod.clients[source]):
        return

    for module in cod.modules:
        cod.notice(source, "%s: %s" % (cod.modules[module].NAME, cod.modules[module].DESC))

    cod.notice(source, "End of module list, %d modules loaded" % len(cod.modules))

def commandMODLOAD(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.client, cod.clients[source]):
        return

    if len(splitline) < 2:
        cod.notice(source, "Need name of module")
        return

    target = splitline[1].lower()

    if target in cod.modules:
        cod.notice(source, "Module %s is loaded" % target)
        return

    try:
        cod.loadmod(target)
    except ImportError as e:
        cod.reply(source, destination, "Module %s failed load: %s" % (target, e))
        return

    cod.servicesLog("MODLOAD:%s: %s" % (target, cod.clients[source].nick))

def commandMODUNLOAD(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.client, cod.clients[source]):
        return

    if len(splitline) < 2:
        cod.notice(source, "Need name of module")
        return

    target = splitline[1].lower()

    if target not in cod.modules:
        cod.notice(source, "Module %s is not loaded" % target)
        return

    try:
        cod.unloadmod(target)
    except Exception as e:
        cod.reply(source, destination, "Module %s failed unload: %s" % (target, e))
        return

    cod.servicesLog("MODUNLOAD:%s: %s" % (target, cod.clients[source].nick))

def commandLISTCHANS(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.client, cod.clients[source]):
        return

    cur = cod.db.cursor()
    cur.execute("SELECT * FROM Joins;")

    rows = cur.fetchall()

    if rows == []:
        cod.notice(source, "No channel joins in database")
        return

    for row in rows:
        cod.notice(source, "AUTOJOIN: %d - %s" % (row[0], row[1]))

    cod.notice(source, "End of channel list")

def logREHASH(cod, line, splitline, source):
    if splitline[3] == "REHASH":
        cod.rehash()

        cod.servicesLog("REHASH: %s" % cod.clients[source].nick)

def handleMOTD(cod, line, splitline, source):
    global motd

    for line in motd:
        cod.notice(source, "MOTD: %s" % line)

    cod.notice(source, "End of /MOTD")

def commandVERSION(cod, line, splitline, source, destination):
    cod.notice(source, "Cod version %s" % cod.version)
