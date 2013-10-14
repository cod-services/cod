"""
Copyright (c) 2013, Sam Dodrill
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

  Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

