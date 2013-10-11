from structures import *

def failIfNotOper(cod, client):
    if not client.isOper:
        cod.notice(client.uid, "Insufficient permissions")
        return True
    else:
        return False

def reply(cod, source, destination, line):
    if source == destination:
        cod.notice(source, line)
    else:
        cod.privmsg(destination, line)

