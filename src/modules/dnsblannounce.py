def initModule(cod):
    cod.s2scommands["ENCAP"].append(announceDNSBLHits)

def destroyModule(cod):
    idx = cod.s2scommands["ENCAP"].index(announceDNSBLHits)
    cod.s2scommands.pop(idx)

def announceDNSBLHits(cod, line, splitline, source):
    if splitline[3] == "SNOTE":
        if splitline[4] == "r":
            cod.servicesLog("DNSBL:HIT: %s" % line.split(":")[2])
