NAME="Rehash"
DESC="Handles the REHASH command"

def initModule(cod):
    cod.s2scommands["ENCAP"] = [logREHASH]

def destroyModule(cod):
    idx = cod.s2scommands["ENCAP"].index(logREHASH)
    cod.s2scommands.pop(idx)

def logREHASH(cod, line, splitline, source):
    if splitline[3] == "REHASH":
        cod.rehash()

        cod.servicesLog("REHASH: %s" % cod.clients[source].nick)

