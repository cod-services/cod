def initModule(cod):
    cod.s2scommands["PRIVMSG"].append(relayHostServToOpers)

def destroyModule(cod):
    idx = cod.s2scommands.index(relayHostServToOpers)
    cod.s2scommands.pop(idx)

def relayHostServToOpers(cod, line, splitline, source):
    if splitline[2] == "#services":
        if cod.clients[source].nick == "HostServ":
            cod.sendLine(cod.client.privmsg(cod.config["etc"]["staffchan"],
                "HostServ: " + " ".join (splitline[3:])[1:]))

