def initModule(cod):
    cod.s2scommands["KILL"].append(logKills)

def destroyModule(cod):
    cod.s2scommands.pop(logKills)

def logKills(cod, line, splitline, source):
    victim = cod.clients[splitline[2]]
    killer = cod.clients[source]

    cod.clients.pop(victim.uid)

    if killer.nick != "NickServ":
        cod.servicesLog("%s: KILL %s %s" % (killer.nick, victim.nick, splitline[4]))

