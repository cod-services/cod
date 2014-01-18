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

NAME="Dogecoin to BTC exchange"
DESC="Wow, such currency"

def initModule(cod):
    cod.addBotCommand("DOGE", priceCheck)

def destroyModule(cod):
    cod.delBotCommand("DOGE")

def rehash():
    pass

def priceCheck(cod, line, splitline, source, destination):
    "Shows Dogecoin exchange rates"

    try:
        info = requests.get("http://pubapi.cryptsy.com/api.php?method=singlemarketdata&marketid=132").json()
        info = info["return"]["markets"]["DOGE"]

        cod.reply(source, destination, "%s to %s prices: %s %s/%s" %
                (info["primaryname"], info["secondaryname"],
                    info["lasttradeprice"], info["primarycode"],
                    info["secondarycode"]))

    except Exception as e:
        cod.reply(source, destination, "There was some error looking dogecoin prices: %s" % e.message)

