def initModule(cod):
    cod.s2scommands["ENCAP"].append(announceDNSBLHits)

def destroyModule(cod):
    cod.s2scommands.pop(announceDNSBLHits)

def announceDNSBLHits(cod, line, splitline, source):
    if splitline[3] == "SNOTE":
        if splitline[4] == "r":
            cod.servicesLog("DNSBL:HIT: %s" % line.split(":")[2])
