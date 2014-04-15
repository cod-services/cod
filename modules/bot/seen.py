"""
Copyright (c) 2014, Xe
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

NAME = "seen"
DESC = "Shows last seen date of an account on NickServ"

from xmlrpclib import Fault


def initModule(cod):
    cod.addBotCommand("SEEN", commandSEEN)


def destroyModule(cod):
    cod.delBotCommand("SEEN")


def commandSEEN(cod, line, splitline, source, destination):
    "Shows you when NickServ last saw a user - Params: account to look up"

    if len(splitline) < 2:
        cod.reply(source, destination, "Params: account to look up")

    account = splitline[1]

    try:
        info = cod.services.nickserv.get_info(account)

        if info["Last seen"] == "now":
            return "%s is online." % account
        else:
            return "%s was last seen %s with quit reason: %s" %\
                   (account, info["Last seen"], info["Last quit"])

    except Fault:
        cod.reply(source, destination, "%s is unknown to me" % account)
    except Exception:
        raise
