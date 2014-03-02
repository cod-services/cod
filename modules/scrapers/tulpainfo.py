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

from bs4 import BeautifulSoup as Soup
import requests
import re
import traceback
import sys

NAME="Tulpa.info"
DESC="Tulpa.info thread title lookups"

TULPAINFO_REGEX = re.compile('community\.tulpa\.info.([-A-Za-z0-9]+)')

def initModule(cod):
    cod.addHook("chanmsg", tulpaInfoLookup)

def destroyModule(cod):
    cod.delHook("chanmsg", tulpaInfoLookup)

def rehash():
    pass

def tulpaInfoLookup(cod, target, line):
    global TULPAINFO_REGEX

    if line.args[0] not in cod.client.channels:
        return

    chatline = line.args[-1]

    if "community.tulpa.info" not in chatline:
        return

    videoid = None

    try:
        threadid = TULPAINFO_REGEX.split(chatline)[1]
    except:
        return

    try:
        info = requests.get("http://community.tulpa.info/%s" % threadid)
        soup = Soup(info.text)

        title = soup("span", "active")[0].text.encode("ascii", "ignore")
        poster = soup("strong")[4].text.encode("ascii", "ignore")
        summary = soup("meta")[3]["content"].encode("ascii", "ignore")

        string = "^ Tulpa.info forums: %s posted %s: %s" %\
            (poster, title, summary)

        cod.privmsg(line.args[0], string)
    except Exception as e:
        cod.privmsg(line.args[0], "There was some error looking up that thread: %s" % e.message)
        traceback.print_exc(file=sys.stdout)

