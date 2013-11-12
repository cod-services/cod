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

NAME="Sendfile"
DESC="allows you to send people files"

from utils import *

def initModule(cod):
    cod.botcommands["SENDFILE"] = [sendfileCMD]

def destroyModule(cod):
    del cod.botcommands["SENDFILE"]

def rehash():
    pass

def sendfileCMD(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.client, cod.clients[source]):
        return

    if len(splitline) < 3:
        cod.reply(source, destination, "SENDFILE <target> <path>")
        return

    with open("etc/sendfile/" + splitline[2], "r") as f:
        for line in f:
            if line.endswith("\n"):
                line = line[:-1]
            elif line.endswith("\r"):
                line = line[:-1]

            cod.privmsg(splitline[1], line)

    cod.servicesLog("%s: SENDFILE %s: %s" %
            (cod.clients[source].nick, splitline[1], splitline[2]))

