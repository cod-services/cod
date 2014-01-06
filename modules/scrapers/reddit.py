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

NAME="Reddit lookups"
DESC="Reddit post info lookups"

# http://www.reddit.com/r/technology/comments/1tey5l/a_solar_boom_in_hawaii_proved_so_successful_that/
REDDIT_REGEX = re.compile('http://reddit.com/r/([\w-]+)/comments/([\w-]+)')

def initModule(cod):
    cod.s2scommands["PRIVMSG"].append(redditLookup)

def destroyModule(cod):
    cod.s2scommands["PRIVMSG"].remove(redditLookup)

def rehash():
    pass

def redditLookup(cod, line):
    global REDDIT_REGEX

    if line.args[0] not in cod.channels:
        return

    client = cod.clients[line.source]
    chatline = line.args[-1]

    songid = None

    try:
        postid = REDDIT_REGEX.split(chatline)[2]
    except:
        return

    try:
        info = requests.get("http://reddit.com/%s/.json" % postid).json()

        title = info[0]["data"]["children"][0]["data"]["title"]
        board = info[0]["data"]["children"][0]["data"]["subreddit"]
        author = info[0]["data"]["children"][0]["data"]["author"]
        url = info[0]["data"]["children"][0]["data"]["url"]

        link = " - URL: %s" % url

        if url in chatline:
            link = ""

        string = "^ Reddit: %s posted to %s: %s%s" %\
                (author, board, title, link)

        cod.privmsg(line.args[0], string)
    except Exception as e:
        cod.privmsg(line.args[0], "There was some error looking up that post: %s" % e.message)

