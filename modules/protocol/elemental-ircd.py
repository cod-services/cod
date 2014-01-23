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

NAME="elemental-ircd protocol module"
DESC="Handles login and protocol commands for elemental-ircd"

CHANMODES=["eIbq", "k" ,"flj" ,"CDEFGJKLMOPQTcdgimnpstz", "yaohv"]

def initModule(cod):
    cod.loginFunc = login

    cod.loadmod("charybdis")

def destroyModule(cod):
    del cod.loginFunc
    cod.loginFunc = None

def rehash():
    pass

def login(cod):
    """
    Sends the commands needed to authenticate to the remote IRC server.
    """

    cod.sendLine("PASS %s TS 6 :%s" % \
            (cod.config["uplink"]["pass"], cod.sid))
    cod.sendLine("CAPAB :QS EX IE KLN UNKLN ENCAP SERVICES EUID EOPMOD")
    cod.sendLine("SERVER %s 1 :%s" % \
            (cod.config["me"]["name"], cod.config["me"]["desc"]))

