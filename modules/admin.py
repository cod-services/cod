from utils import *
from structures import *

NAME="Admin"
DESC="Administrative commands"

def initModule(cod):
    cod.botcommands["JOIN"] = [commandJOIN]
    cod.botcommands["PART"] = [commandPART]
    cod.botcommands["REHASH"] = [commandREHASH]
    cod.botcommands["DIE"] = [commandDIE]
    cod.botcommands["MODLOAD"] = [commandMODLOAD]
    cod.botcommands["MODLIST"] = [commandMODLIST]
    cod.botcommands["MODUNLOAD"] = [commandMODUNLOAD]

    cur = cod.db.cursor()

    cur.execute("PRAGMA table_info(Joins);")

    pragma = cur.fetchall()

    if pragma == []:
        cur.execute("CREATE TABLE Joins(Id INTEGER PRIMARY KEY, Name TEXT);")
        cod.db.commit()

    cur.execute("SELECT * FROM Joins;")

    rows = cur.fetchall()

    if rows == []:
        return

    for row in rows:
        cod.join(row[1])

def destroyModule(cod):
    del cod.botcommands["JOIN"]
    del cod.botcommands["PART"]
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
        cod.notice(source, "I have joined %s" % channel)

        cur = cod.db.cursor()

        cur.execute("INSERT INTO Joins(Name) VALUES ('%s');" % channel)

        cod.db.commit()

    else:
        cod.notice(source, "USAGE: JOIN #channel")

def commandPART(cod, line, splitline, source, destination):
     if failIfNotOper(cod, cod.clients[source]):
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
    if failIfNotOper(cod, cod.clients[source]):
        return

    cod.rehash()

    client = cod.clients[source]
    cod.servicesLog("REHASH: %s" % client.nick)

def commandDIE(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    cod.servicesLog("DIE: %s" % cod.clients[source].nick)

    cod.db.close()

    cod.sendLine(cod.client.quit())

    cod.sendLine("SQUIT")

def commandMODLIST(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
        return

    for module in cod.modules:
        cod.notice(source, "%s: %s" % (cod.modules[module].NAME, cod.modules[module].DESC))

    cod.notice(source, "End of module list")

def commandMODLOAD(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients[source]):
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
    if failIfNotOper(cod, cod.clients[source]):
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

