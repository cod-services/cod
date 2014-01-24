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

NAME="Vimeo lookups"
DESC="Vimeo title lookups"

VIMEO_REGEX = re.compile('vimeo.com/([0-9]+)')

def initModule(cod):
    cod.s2scommands["PRIVMSG"].append(vimeoLookup)

def destroyModule(cod):
    cod.s2scommands["PRIVMSG"].remove(vimeoLookup)

def rehash():
    pass

def vimeoLookup(cod, line):
    global VIMEO_REGEX

    if line.args[0] not in cod.channels:
        return

    chatline = line.args[-1]

    if "vimeo" not in chatline:
        return

    videoid = None

    try:
        videoid = VIMEO_REGEX.split(chatline)[1]
    except:
        return

    try:
        info = requests.get("http://vimeo.com/api/v2/video/%s.json" % videoid).json()

        string = "^ Vimeo: %s" % info[0]["title"]

        cod.privmsg(line.args[0], string)
    except Exception as e:
        cod.privmsg(line.args[0], "There was some error looking up that video: %s" % e.message)

