NAME="Version"
DESC="Shows the version of this Cod instance"

def initModule(cod):
    cod.botcommands["VERSION"] = [commandVERSION]

def destroyModule(cod):
    del cod.botcommands["VERSION"]

def commandVERSION(cod, line, splitline, source, destination):
    cod.notice(source, "Cod version %s" % cod.version)

