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

NAME="Source Code Linker"
DESC="It just replies with a link to the github repo"

def initModule(cod):
    cod.addBotCommand("SOURCE", testbotCommand)

def destroyModule(cod):
    cod.delBotCommand("SOURCE")

def testbotCommand(cod, line, splitline, source, destination):
    "Shows source code information"
    cod.reply(source, destination, "I am an instance of Cod version %s running on %s. You can find more information about me at http://github.com/cod-services/cod" %\
            (cod.version, cod.config["uplink"]["protocol"]))

