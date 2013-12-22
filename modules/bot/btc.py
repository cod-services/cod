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

import requests

NAME="MTGox price lookups"
DESC="Shows the BTC price on MTGox"

def initModule(cod):
    cod.addBotCommand("BTC", priceCheck)

def destroyModule(cod):
    cod.delBotCommand("BTC")

def rehash():
    pass

def priceCheck(cod, line, splitline, source, destination):
    try:
        info = requests.get("http://data.mtgox.com/api/2/BTCUSD/money/ticker").json()

        cod.reply(source, destination, "MtGox prices: Average: %s, High: %s, Low: %s" %\
                (info["data"]["avg"]["display"], info["data"]["high"]["display"],
                    info["data"]["low"]["display"]))
    except Exception as e:
        cod.reply(source, destination, "There was some error looking bitcoin prices: %s" % e.message)

