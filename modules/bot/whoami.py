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

NAME="whoami"
DESC="Shows information about yourself"

def initModule(cod):
    cod.addBotCommand("WHOAMI", commandWHOAMI)

def destroyModule(cod):
    cod.delBotCommand("WHOAMI")

def rehash():
    pass

def commandWHOAMI(cod, line, splitline, source, destination):
    "Shows you what cod thinks it knows about you"

    try:
        oper = "Oper" if source.isOper else "User"

        string = "%s %s!%s@%s: %s%s: %s" %\
                (oper, source.nick, source.user, source.host, source.gecos,
                        source.login)

        cod.reply(source, destination, string)
    except Exception as e:
        cod.log("%s %s" % (type(e), e.message))

