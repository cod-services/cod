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

NAME="Soundcloud lookups"
DESC="Soundcloud song info lookups"

SOUNDCLOUD_REGEX = re.compile('http://(soundcloud.com/)([\w-]+)/([\w-]+)')

def initModule(cod):
    cod.s2scommands["PRIVMSG"].append(soundcloudLookup)

def destroyModule(cod):
    cod.s2scommands["PRIVMSG"].remove(soundcloudLookup)

def rehash():
    pass

def soundcloudLookup(cod, line):
    global SOUNDCLOUD_REGEX

    if line.args[0] not in cod.channels:
        return

    chatline = line.args[-1]

    songid = None

    try:
        songid = SOUNDCLOUD_REGEX.split(chatline)[3]
        artist = SOUNDCLOUD_REGEX.split(chatline)[2]
    except:
        return

    try:
        info = requests.get("http://soundcloud.com/oembed?format=json&url=https:%%2f%%2fsoundcloud.com%%2f%s%%2f%s" % (artist,songid)).json()

        string = "^ Soundcloud: %s" % info["title"]

        cod.privmsg(line.args[0], string)
    except Exception as e:
        cod.privmsg(line.args[0], "There was some error looking up that song: %s" % e.message)

