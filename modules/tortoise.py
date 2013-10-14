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

import requests
from structures import *
from utils import *

NAME="Tortoise Labs interface"
DESC="Interface to tortoise labs API"

"""
Prints DNS pool information when your pool is set up on Tortoise Labs.
"""

global client

def initModule(cod):
    global client

    client = makeService(cod.config["dns"]["nick"], cod.config["dns"]["user"],
            cod.config["dns"]["host"], cod.config["dns"]["gecos"],
            cod.config["uplink"]["sid"] + "DNSSRV")

    cod.s2scommands["PRIVMSG"].append(handleMessages)

    cod.clients[client.uid] = client

    cod.sendLine(client.burst())

    cod.sendLine(client.join(cod.channels[cod.config["etc"]["snoopchan"]]))
    cod.sendLine(client.join(cod.channels[cod.config["etc"]["staffchan"]]))

def destroyModule(cod):
    global client

    idx = cod.s2scommands["PRIVMSG"].index(handleMessages)
    cod.s2scommands["PRIVMSG"].pop(idx)

    cod.sendLine(client.quit())

    cod.clients.pop(client.uid)

def handleMessages(cod, line, splitline, source):
    global client

    if splitline[2] != client.uid:
        return

    line = ":".join(line.split(":")[2:])
    splitline = line.split()

    if splitline[0].upper() == "POOL":
        if failIfNotOper(cod, client, cod.clients[source]):
            return

        auth = (cod.config["tortoiselabs"]["username"],
                cod.config["tortoiselabs"]["apikey"])

        request = requests.get("http://manage.tortois.es/dns/zones", auth=auth)

        for line in request.json["zones"]:
            if line["name"] == cod.config["dns"]["name"]:
                for record in line["records"]:
                    if record["name"] == cod.config["dns"]["pool"]:
                        cod.sendLine(client.privmsg(source, record["content"]))
                cod.sendLine(client.privmsg(source, "End of pool %s" % cod.config["dns"]["pool"]))

    else:
        cod.sendLine(client.notice(source, "Valid commands are:"))
        cod.sendLine(client.notice(source, " - POOL: Show DNS pool"))

