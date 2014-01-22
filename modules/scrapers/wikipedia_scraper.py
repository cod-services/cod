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
import wikipedia

from niilib.url_decode import urldecode
from textwrap import wrap

NAME="Wikipedia lookups"
DESC="Does %s" % NAME

#https://en.wikipedia.org/wiki/Samhain
WIKIPEDIA_REGEX = re.compile('(en.wikipedia.org/wiki/)([\w-]+)')

def initModule(cod):
    cod.s2scommands["PRIVMSG"].append(wikipediaLookup)

def destroyModule(cod):
    cod.s2scommands["PRIVMSG"].remove(wikipediaLookup)

def rehash():
    pass

def wikipediaLookup(cod, line):
    global WIKIPEDIA_REGEX

    if line.args[0] not in cod.channels:
        return

    chatline = line.args[-1]

    songid = None

    try:
        article = WIKIPEDIA_REGEX.split(chatline)[2]
    except:
        return

    try:
        info = wikipedia.page(urldecode(article))

        content = info.content

        if len(content) > 150:
            content = wrap(info.content, 150)[0]

        string = "^ Wikipedia: %s - %s..." %\
                (info.title, ''.join([x for x in content if ord(x) < 128]))

        cod.privmsg(line.args[0], string)
    except Exception as e:
        cod.privmsg(line.args[0], "There was some error looking up that article: %s %s" % (type(e), e.message))

