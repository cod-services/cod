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

NAME="FAQ Service"
DESC="Stores responses to frequently asked questions"

from structures import *
from utils import *

global client

def initModule(cod):
    global client

    client = makeService(cod.config["faq"]["nick"], cod.config["faq"]["user"],
            cod.config["faq"]["host"], cod.config["faq"]["gecos"],
            cod.getUID())

    cod.addBotCommand("FAQ", commandFAQ, True)

    initDBTable(cod, "FAQ",
            "Id INTEGER PRIMARY KEY, Name TEXT, Content TEXT")

    cod.clients[client.uid] = client

    cod.sendLine(client.burst())

    cod.log("Bursting FAQ client", "!!!")

    cod.sendLine(client.join(cod.channels[cod.config["etc"]["snoopchan"]]))
    cod.sendLine(client.join(cod.channels[cod.config["etc"]["helpchan"]]))

def destroyModule(cod):
    global client

    cod.sendLine(client.quit())
    cod.clients.pop(client.uid)

    cod.delBotCommand("FAQ")

def rehash():
    pass

def commandFAQ(cod, line, splitline, source, destination):
    global client

    if failIfNotOper(cod, client, cod.clients[source]):
        return

    if len(splitline) < 2:
        cod.notice(source, "At least 2 parameters needed", client)
        return

    if splitline[1].upper() == "ADD":
        if len(splitline) < 4:
            cod.notice(source, "At least 3 parameters needed", client)
            cod.notice(source, "ADD Topic Content of topic", client)
            return

        name = splitline[2].upper()
        content = " ".join(splitline[3:])

        cur = cod.db.cursor()

        cur.execute("INSERT INTO FAQ(Name, Content) VALUES ('%s', '%s');" %
                (name, content))

        cod.db.commit()

        cod.notice(source, "FAQ topic %s added: \"%s\"" %
                (name, content), client)
        cod.servicesLog("FAQ:ADD: %s \"%s\" -- %s" %
                (name, content, cod.clients[source].nick))

    elif splitline[1].upper() == "LIST":
        cur = cod.db.cursor()
        cur.execute("SELECT * FROM FAQ;")
        rows = cur.fetchall()

        topics = []

        for row in rows:
            topics.append(row[1])

        cod.notice(source, "Topics: %s" % " ".join(topics))

    else:
        if len(splitline) < 2:
            cod.notice(source, "Invalid syntax", client)
            return

        topic = splitline[1]

        cur = cod.db.cursor()
        cur.execute("SELECT * FROM FAQ;")
        rows = cur.fetchall()

        for row in rows:
            if row[1] == topic.upper():
                cod.sendLine(client.privmsg(destination, "%s: %s") %
                    (topic, row[2]))
                return

        cod.sendLine(client.notice(source, "Topic %s not found" % topic))

