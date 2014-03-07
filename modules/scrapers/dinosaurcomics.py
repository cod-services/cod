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
import traceback
import sys

NAME="Dinosaur comics"
DESC="Dinosaur comic title lookup"

DINOCOMIC_REGEX = re.compile('qwantz.com/index.php\?comic\=([0-9]+)')

def initModule(cod):
    cod.addHook("chanmsg", dinoComicLookup)

def destroyModule(cod):
    cod.delHook("chanmsg", dinoComicLookup)

def dinoComicLookup(cod, target, line):
    global DINOCOMIC_REGEX

    if line.args[0] not in cod.client.channels:
        return

    chatline = line.args[-1]

    if "qwantz" not in chatline:
        return

    comicid = ""

    try:
        comicid = DINOCOMIC_REGEX.split(chatline)[1]
    except:
        traceback.print_exc(file=sys.stdout)

    try:
        info = requests.get("http://www.qwantz.com/index.php?comic=%s" % comicid)
        soup = Soup(info.text)

        title = soup("img", "comic")[0].get("title")
        date = soup("title")[0].text.split(" - ")[1]

        string = "^ Dinosaur comics: #%s %s - %s" % (comicid, date, title)

        cod.privmsg(line.args[0], string)
    except:
        traceback.print_exc(file=sys.stdout)

