NAME="RESV logger"
DESC="Logs the use of RESV commands"

def initModule(cod):
    cod.s2scommands["ENCAP"] = [logRESV]

def destroyModule(cod):
    idx = cod.s2scommands["ENCAP"].index(logRESV)
    cod.s2scommands.pop(idx)

def logRESV(cod, line, splitline, source):
    if splitline[3] == "RESV":
        if splitline[2] == "0":
            cod.servicesLog("RESV: %s -- INFINITE by: %s" %
                    (splitline[3], cod.clients[source].nick))
        else:
            time = int(splitline[4])
            time = time / 60

            cod.servicesLog("RESV: %s %d minutes by: %s" %
                    (splitline[5], time, cod.clients[source].nick))

