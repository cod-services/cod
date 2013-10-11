def initModule(cod):
    cod.s2scommands["PRIVMSG"].append(prettyPrintMessages)

def destroyModule(cod):
    idx = cod.s2scommands.index(prettyPrintMessages)
    cod.s2scommands.pop(idx)

def prettyPrintMessages(cod, line, splitline, source):
    if not cod.config["etc"]["production"]:
        client = cod.clients[source]

        print "{0}: <{1}> {2}".format(splitline[2], client.nick, " ".join (splitline[3:])[1:])
