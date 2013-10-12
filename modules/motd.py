NAME="MOTD handler"
DESC="Handles the MOTD command"

global motd

motd = []

def initModule(cod):
    global motd

    motd = []

    cod.s2scommands["MOTD"] = [handleMOTD]

    with open(cod.config["me"]["motd"], "r") as fin:
        cod.log("reading MOTD from %s" % cod.config["me"]["motd"], "===")
        for line in fin.readlines():
            motd.append(line.strip())

def destroyModule(cod):
    global motd

    del cod.s2scommands["MOTD"]
    del motd

def handleMOTD(cod, line, splitline, source):
    global motd

    for line in motd:
        cod.notice(source, "MOTD: %s" % line)

    cod.notice(source, "End of /MOTD")

