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
import re

NAME="Derpibooru lookups"
DESC="Derpibooru image info lookups"

DERPI_REGEX = re.compile('(derpiboo.ru/)([\w-]+)')

def initModule(cod):
    cod.s2scommands["PRIVMSG"].append(derpiLookup)

def destroyModule(cod):
    cod.s2scommands["PRIVMSG"].remove(derpiLookup)

def rehash():
    pass

def derpiLookup(cod, line):
    global DERPI_REGEX

    if line.args[0] not in cod.channels:
        return

    chatline = line.args[-1]

    if "derpi" not in chatline:
        return

    imageid = None

    try:
        imageid = DERPI_REGEX.split(chatline)[2]
    except:
        return

    try:
        info = requests.get("http://derpiboo.ru/%s.json?nocomments&" % imageid).json()

        tags = info["tags"]
        nsfw = "explicit" in tags

        string = "^ Derpibooru: %s - Score: %s (+%s -%s) - %s" % (info["tags"],
                info["score"], info["upvotes"], info["downvotes"], "NSFW" if nsfw else "SFW")

        cod.privmsg(line.args[0], string)
    except Exception as e:
        cod.privmsg(line.args[0], "There was some error looking up that image: %s" % e.message)

