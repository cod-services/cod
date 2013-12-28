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

from utils import *
from structures import *

NAME="dnsbl"
DESC="Does DNSBL lookups by nick or IP address"

import rblwatch

def initModule(cod):
    cod.addBotCommand("RBL", commandRBL, True)

def destroyModule(cod):
    cod.delBotCommand("RBL")

def rehash():
    pass

def commandRBL(cod, line, splitline, source, destination):
    "USAGE: RBL [nick or IP address to scan]"

    if len(splitline) < 2:
        cod.notice(source, "USAGE: RBL [nick or IP address to scan]")
        return

    search = None
    target = splitline[1]

    if splitline[1].find(".") == -1:
        #If we don't have an IP address, we have a nick of a client
        mark = None

        client = cod.findClientByNick(target)

        if client == None:
            cod.notice(source, "Error: %s is not on IRC" % mark)
            return

        if client.ip == "0":
            cod.notice(source, "Error: target %s is a network service" % client.nick)
            return

        target = client.ip

    cod.servicesLog("RBL: %s: %s" % (target, source.nick))

    search = rblwatch.RBLSearch(cod, target)

    search.print_results()

