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

import requests

NAME="Dota 2 hero count"
DESC="Dota 2 hero counter"

def initModule(cod):
    cod.addBotCommand("DOTACOUNT", dotaCheck)

def destroyModule(cod):
    cod.delBotCommand("DOTACOUNT")

def rehash():
    pass

def dotaCheck(cod, line, splitline, source, destination):
    "Shows the number of heroes in Dota's roster"

    try:
        info = requests.get("https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?key=%s" %\
                cod.config["apikeys"]["steam"]).json()

        cod.reply(source, destination, "%d heroes in Dota at this time." %\
                info["result"]["count"])

    except Exception as e:
        cod.reply(source, destination, "There was some error looking that up: %s" % e.message)

