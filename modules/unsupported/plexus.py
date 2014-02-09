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

import sys

from structures import *
from utils import *

NAME="plexus protocol module"
DESC="Handles login and protocol commands for PleXus"

CHANMODES=["eIb", "k" ,"l" ,"BCMNORScimnpstz", "qaohv"]

def initModule(cod):
    cod.loginFunc = login
    cod.burstClient = burstClient

    cod.s2scommands["UID"] = [handleUID]

    cod.loadmod("charybdis")

def destroyModule(cod):
    del cod.loginFunc
    cod.loginFunc = None

    del cod.s2scommands["UID"]

def rehash():
    pass

def login(cod):
    """
    Sends the commands needed to authenticate to the remote IRC server.
    """

    cod.sendLine("PASS %s TS 6 :%s" % \
            (cod.config["uplink"]["pass"], cod.sid))
    cod.sendLine("CAPAB :QS EX CHW IE EOB KLN UNKLN GLN HUB KNOCK TBURST PARA ENCAP SVS")
    cod.sendLine("SERVER %s 1 :%s" % \
            (cod.config["me"]["name"], cod.config["me"]["desc"]))

def handleUID(cod, line):
    nick, ts, modes, user, ip, host, uid, gecos = line.args[0], line.args[2], \
        line.args[3], line.args[4], line.args[5], line.args[6], line.args[8], \
        line.args[-1]

    client = Client(nick, uid, ts, modes, user. host, ip, "*", gecos)

    cod.clients[uid] = client

def burstClient(cod, client):
    # UplinkSocket::Message(Me) << "UID " << u->nick << " 1 " << u->timestamp << " " << modes << " " << u->GetIdent() << " " << u->host << " 255.255.255.255 " << u->GetUID() << " 0 " << u->host << " :" << u->realname;
    burst = ":%s UID %s 1 %d +iUo %s %s 0 %s 0 %s :%s" %\
        (cod.sid, client.nick, int(time.time), client.user, client.host,
                client.uid, client.host, client.gecos)
    cod.sendLine(burst)

