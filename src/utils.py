from structures import *

def failIfNotOper(cod, client, dest):
    """
    Checks if the client passed in an argument is an IRC operator and returns
    True **IF THEY ARE NOT AN OPERATOR***
    """
    if not dest.isOper:
        cod.sendLine(client.notice(dest.uid, "Insufficient permissions"))
        return True
    else:
        return False

def initDBTable(cod, tabname, format):
    cur = cod.db.cursor()
    cur.execute("PRAGMA table_info(%s);" % tabname)

    pragma = cur.fetchall()
    if pragma == []:
        cur.execute("CREATE TABLE %s(%s);" %(tabname, format))
        cod.db.commit()

