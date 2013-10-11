from structures import *

def failIfNotOper(cod, client):
    """
    Checks if the client passed in an argument is an IRC operator and returns
    True **IF THEY ARE NOT AN OPERATOR***
    """
    if not client.isOper:
        cod.notice(client.uid, "Insufficient permissions")
        return True
    else:
        return False

