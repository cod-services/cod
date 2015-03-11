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

import htmllib
import requests
import re

NAME="4chan lookups"
DESC="4chan post info lookups"

FOURCHAN_REGEX = re.compile('(.+boards\.)4chan\.org\/([a-z0-9]+)\/res\/([1-9][0-9]+)')

def initModule(cod):
    cod.s2scommands["PRIVMSG"].append(fourchanLookup)

def destroyModule(cod):
    cod.s2scommands["PRIVMSG"].remove(fourchanLookup)

def rehash():
    pass

def unescape(comment):
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(comment)
    return p.save_end()

# http://stackoverflow.com/a/14464381
def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out

def fourchanLookup(cod, line):
    """
    This uses requests to scrape out things from the 4chan API
    """

    global FOURCHAN_REGEX

    if line.args[0] not in cod.channels:
        return

    chatline = line.args[-1]

    postid = None

    try:
        board = FOURCHAN_REGEX.split(chatline)[2]
        postid = FOURCHAN_REGEX.split(chatline)[3]
    except:
        return

    try:
        info = requests.get("http://api.4chan.org/%s/res/%s.json" % (board, postid)).json()

        text = info["posts"][0]["com"].split("<br>")[0]

        text = unescape(remove_html_markup(post))

        string = "^ 4chan: %s on /%s/ - %s%s - %s" %\
                (info["posts"][0]["name"], board, info["posts"][0]["filename"],
                        info["posts"][0]["ext"], text)

        cod.privmsg(line.args[0], string)
    except Exception as e:
        cod.privmsg(line.args[0], "There was some error looking up that post: %s" % e.message)

