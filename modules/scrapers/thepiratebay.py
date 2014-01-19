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
import re
from bs4 import BeautifulSoup

NAME="The Pirate Bay scraper"
DESC="TPB torrent lookups"

TPB_REGEX = re.compile('(thepiratebay\..*)/torrent/([\w-]+)')

def initModule(cod):
    cod.s2scommands["PRIVMSG"].append(thepiratebayLookup)

def destroyModule(cod):
    cod.s2scommands["PRIVMSG"].remove(thepiratebayLookup)

def rehash():
    pass

def thepiratebayLookup(cod, line):
    global TPB_REGEX

    if line.args[0] not in cod.channels:
        return

    chatline = line.args[-1]

    torrentid = None

    try:
        torrentid = TPB_REGEX.split(chatline)[2]
    except:
        return

    try:
        info = requests.get("https://thepiratebay.se/torrent/%s" % torrentid).text
        soup = BeautifulSoup(info)

        link = filter((lambda x: x["href"].startswith("magnet")),
                soup.find_all('a', href=True))[0]["href"][:60]

        title = soup.find_all("title")[0].text.split("(download")[0].strip()

        string = "^ The Pirate Bay: %s - %s" % (title, link)

        cod.privmsg(line.args[0], string)
    except Exception as e:
        cod.privmsg(line.args[0], "There was some error looking up that torrent: %s" % e.message)

