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

import time
import random

NAME="Choice bot command"
DESC="Picks from a user-supplied, comma-delineated list of things"

def initModule(cod):
    cod.botcommands["CHOICE"] = [commandCHOICE]

def destroyModule(cod):
    del cod.botcommands["CHOICE"]

def rehash():
    pass

def commandCHOICE(cod, line, splitline, source, destination):
    choices = " ".join(splitline[1:])
    choices = choices.split(", ")

    if len(choices) == 0 or len(choices) == 1:
        cod.reply(source, destination, "BAD " + cod.clients[source].nick)
        return

    choice = random.choice(choices)

    cod.reply(source, destination, "Result: " + choice)

