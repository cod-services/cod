import rblwatch

def initModule(cod):
    cod.s2scommands["ENCAP"].append(announceDNSBLHits)

def destroyModule(cod):
    idx = cod.s2scommands["ENCAP"].index(announceDNSBLHits)
    cod.s2scommands.pop(idx)

def announceDNSBLHits(cod, line, splitline, source):
    if splitline[3] == "SNOTE":
        if splitline[4] == "r":
            message = line.split(":")[2]
            cod.servicesLog("DNSBL:HIT: %s" % message)

            ip = message.split()[1].split("@")[1][:-1]

            cod.servicesLog("Checking %s in %d blacklists..." %(ip, len(rblwatch.RBLS)))

            search = rblwatch.RBLSearch(cod, ip)
            search.print_results()

