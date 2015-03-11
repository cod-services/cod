"""
Copyright (c) 2013, Christine Dodrill
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

NAME="Danbooru lookups"
DESC="Danbooru image info lookups"

DANBOORU_REGEX = re.compile('(danbooru.donmai.us/posts/)([\w-]+)')

def initModule(cod):
    cod.s2scommands["PRIVMSG"].append(danboLookup)

def destroyModule(cod):
    cod.s2scommands["PRIVMSG"].remove(danboLookup)

def rehash():
    pass

def danboLookup(cod, line):
    global DANBOORU_REGEX

    if line.args[0] not in cod.channels:
        return

    chatline = line.args[-1]

    if "danbooru" not in chatline:
        return

    imageid = None

    try:
        imageid = DANBOORU_REGEX.split(chatline)[2]
    except:
        return

    try:
        info = requests.get("http://danbooru.donmai.us/posts/%s.json?nocomments&" % imageid).json()

        tags = ", ".join(info["tag_string"].split())
        nsfw = info["rating"] != "s"

        string = "^ Danbooru: %s - %s" % ("NSFW" if nsfw else "SFW", info["tag_string"])

        cod.privmsg(line.args[0], string)
    except Exception as e:
        cod.privmsg(line.args[0], "There was some error looking up that image: %s" % e.message)

