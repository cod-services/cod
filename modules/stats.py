NAME="STATS command handler"
DESC="Handles the STATS command"

def initModule(cod):
    cod.s2scommands["STATS"] = [handleSTATS]

def destroyModule(cod):
    del cod.s2scommands["STATS"]

def handleSTATS(cod, line, splitline, source):
    if splitline[2] == "v":
        cod.notice(source, "Cod version %s" % cod.version)

    elif splitline[2] == "c":
        cod.notice(source, "%d clients in ram" % len(cod.clients))

    elif splitline[2] == "C":
        cod.notice(source, "%d channels in ram" % len(cod.channels))

    elif splitline[2] == "m":
        cod.notice(source, "%d modules loaded" % len(cod.modules))

    elif splitline[2] == "M":
        cod.notice(source, "%d protocol commands loaded" % len(cod.s2scommands))
        cod.notice(source, "%d bot commands loaded" % len(cod.botcommands))
    else:
        cod.notice(source, "Stats commands: [v]ersion, [c]lients, [C]hannels, [m]modules, co[M]mands")

    cod.notice(source, "End of /STATS report")

