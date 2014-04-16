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

# In an ideal world, this would not be needed.

NAME="killonfailoper"
DESC="Kills clients that fail OPER attempts"
#XXX: Number of tries before kill?

def initModule(cod):
    cod.s2scommands["ENCAP"].append(killOnFailOper)

def destroyModule(cod):
    cod.s2scommands["ENCAP"].remove(killOnFailOper)

def rehash():
    pass

def killOnFailOper(cod, line):
    if not line.args[1] == "SNOTE":
        return

    if not line.args[2] == "s":
        return

    if not line.args[-1].split()[1] == "OPER":
        return

    offendingclient = cod.findClientByNick(line.args[-1].split()[7])

    cod.notice(offendingclient, "You may not attempt to become an operator without being on staff")
    cod.notice(offendingclient, "Staff has been notified. Depending on staff decisions, you might")
    cod.notice(offendingclient, "have additional consequences for this action.")

    cod.servicesLog("%s FAILED OPER attempt: (%s@%s : %s), killed" % (offendingclient.nick,
        offendingclient.user, offendingclient.host, offendingclient.ip))

    cod.kill(offendingclient, cod.client, "(Failed OPER attempt)")

