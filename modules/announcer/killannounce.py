"""
Copyright (c) 2013, Christine Dodrill
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

NAME="kill announce"
DESC="Announces non-services sourced kills to snoop channel"

def initModule(cod):
    cod.s2scommands["KILL"].append(logKills)

def destroyModule(cod):
    cod.s2scommands["KILL"].remove(logKills)

def rehash():
    pass

def logKills(cod, line):
    victim = cod.clients[line.args[0]]
    killer = cod.clients[line.source]

    cod.clients.pop(victim.uid)

    if not killer.nick.endswith("Serv"):
        cod.servicesLog("%s: KILL %s %s" % (killer.nick, victim.nick, line.args[-1]))

