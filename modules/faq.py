NAME="FAQ Service"
DESC="Stores responses to frequently asked questions"

from structures import *
from utils import *

global client

def initModule(cod):
    global client

    client = makeService(cod.config["faq"]["nick"], cod.config["faq"]["user"],
            cod.config["faq"]["host"], cod.config["faq"]["gecos"],
            cod.config["uplink"]["sid"] + "FAQSRV")

    cod.botcommands["FAQ"] = [commandFAQ]

    initDBTable(cod, "FAQ",
            "Id INTEGER PRIMARY KEY, Name TEXT, Content TEXT")

    cod.clients[client.uid] = client

    cod.sendLine(client.burst())

    cod.sendLine(client.join(cod.channels[cod.config["etc"]["snoopchan"]]))

def destroyModule(cod):
    global client

    cod.sendLine(client.quit())
    cod.clients.pop(client.uid)

    del cod.botcommands["FAQ"]

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

