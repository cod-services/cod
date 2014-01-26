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

from structures import *
from utils import *

NAME="INJECT"
DESC="LOL OPER ABUSE"

def initModule(cod):
    if not cod.config["etc"]["production"]:
        cod.addBotCommand("INJECT", inject, True)
    else:
        cod.servicesLog("Cowardly refusing to load INJECT with production mode on")

def destroyModule(cod):
    if not cod.config["etc"]["production"]:
        cod.delBotCommand("INJECT")

def rehash():
    pass

def inject(cod, line, splitline, source, destination):
    "Inject raw commands into the uplink. USE WITH CARE"

    if failIfNotOper(cod, source, destination):
        return

    cod.sendLine(" ".join(splitline[1:]))
    cod.servicesLog("%s INJECT: %s" % (source.nick, " ".join(splitline[1:])))

