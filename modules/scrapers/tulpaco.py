"""
Copyright (c) 2014, Xe
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

from bs4 import BeautifulSoup as Soup
import requests
import re

NAME="Tulpa.co"
DESC="Tulpa.co thread title lookups"

TULPACO_REGEX = re.compile('tulpa.co/showthread.php\?tid\=([0-9]+)')

def initModule(cod):
    cod.addHook("chanmsg", tulpaCoLookup)

def destroyModule(cod):
    cod.delHook("chanmsg", tulpaCoLookup)

def tulpaCoLookup(cod, target, line):
    global TULPACO_REGEX

    if line.args[0] not in cod.client.channels:
        return

    chatline = line.args[-1]

    if "tulpa.co" not in chatline:
        return

    try:
        threadid = TULPACO_REGEX.split(chatline)[1]
    except:
        return

    info = requests.get("http://tulpa.co/showthread.php?tid=%s" % threadid)
    soup = Soup(info.text)

    title = soup("span", "active")[0].text.encode("ascii", "ignore")
    poster = soup("span", "largetext")[0].text.encode("ascii", "ignore")

    string = "^ Tulpa.co forums: %s posted %s" % (poster, title)

    cod.privmsg(line.args[0], string)

