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

from utils import addtoDB

NAME="FunServ join handler"
DESC="Automatically handles joins requested via FunServ"

def initModule(cod):
    cod.s2scommands["NOTICE"] = [handleNOTICE]

def destroyModule(cod):
    del cod.s2scommands["NOTICE"]

def rehash():
    pass

#XXX: I am sorry for this blatant RFC violation
def handleNOTICE(cod, line):
    """
    ***RFC VIOLATION***

    Atheme has no really good way to send out PRIVMSG's, so I have made this
    reply to notices from FunServ for now.
    """

    if cod.clients[line.source].nick.upper() == "FUNSERV":
        args = line.args[1].split()
        if args[0] == "JOIN":
            if args[1] in cod.channels:
                return

            cod.join(args[1])
            addtoDB(cod, "INSERT INTO Joins(Name) VALUES ('%s');" % args[1])

            cod.privmsg(args[1], "Hi! I am a network service bot requested to serve this channel. You can see my list of commands by using the command %shelp. My command prefix is %s." % (cod.config["me"]["prefix"], cod.config["me"]["prefix"]))
            cod.privmsg(args[1], "For additional help or to request more features, please see %s." % cod.config["etc"]["helpchan"])

