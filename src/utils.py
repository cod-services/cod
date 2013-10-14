"""
Copyright (c) 2013, Sam Dodrill
All rights reserved.

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

    1. The origin of this software must not be misrepresented; you must not
    claim that you wrote the original software. If you use this software
    in a product, an acknowledgment in the product documentation would be
    appreciated but is not required.

    2. Altered source versions must be plainly marked as such, and must not be
    misrepresented as being the original software.

    3. This notice may not be removed or altered from any source
    distribution.
"""

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

    pragmaquery = "PRAGMA table_info(%s);" % tabname
    cur.execute(pragmaquery)

    cod.log("DB: %s" % pragmaquery, "===")

    pragma = cur.fetchall()
    if pragma == []:
        query = "CREATE TABLE %s(%s);" %(tabname, format)

        cur.execute(query)
        cod.db.commit()
        cod.log("DB: %s" % query, "===")

def lookupDB(cod, table):
    cur = cod.db.cursor()

    query = "SELECT * FROM %s;" % table

    cur.execute(query)
    cod.log("DB: %s" % query, "===")

    return cur.fetchall()

def deletefromDB(cod, query):
    cur = cod.db.cursor()

    cur.execute(query)
    cod.db.commit()
    cod.log("DB: %s" % query, "===")

def addtoDB(cod, query):
    cur = cod.db.cursor()

    cur.execute(query)
    cod.db.commit()
    cod.log("DB: %s" % query, "===")

