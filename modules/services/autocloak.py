"""
Copyright (c) 2014, Sam Dodrill
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

NAME="Autocloak"
DESC="Manages automatic cloaks for bouncers"

from structures import *
from utils import *

import md5

global client

def initModule(cod):
    global client

    client = makeService(cod.config["autocloak"]["nick"], cod.config["autocloak"]["user"],
            cod.config["autocloak"]["host"], cod.config["autocloak"]["gecos"],
            cod.getUID())

    cod.clients[client.uid] = client

    cod.sendLine(client.burst())
    cod.log("Bursting autocloak client", "!!!")

    cod.s2scommands["EUID"].append(handleCloak)

    cod.sendLine(client.join(cod.channels[cod.config["etc"]["snoopchan"]]))

def destroyModule(cod):
    global client

    cod.sendLine(client.quit())
    cod.clients.pop(client.uid)

def rehash():
    pass

def handleCloak(cod, line):
    #Check user's IP in the autocloak list
    if line.args[6] in cod.config["autocloak"]["list"]:
        #If they are authed, they probably have a vhost or are getting re-bursted
        #so it would be a Bad Idea to cloak them
        if line.args[-2] != "*":
            return

        cloaksuffix = cod.config["autocloak"]["list"][line.args[6]]
        ident = line.args[4]

        m = md5.new()
        m.update(ident)

        unique = m.hexdigest()[:16]

        host = "%s.%s" % (unique.upper(), cloaksuffix)

        cod.sendLine(":%s CHGHOST %s %s" % (client.uid, line.args[7], host))
        cod.notice(line.args[7], "Your vhost has been uniquely randomized as a part of a policy set by your BNC host and network staff. If your desired vhost doesn't show up, please re-activate it using /msg HostServ ON", client)

