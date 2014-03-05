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

NAME="Youtube lookups"
DESC="Youtube searching and title lookups"

YOUTUBE_REGEX = re.compile('(youtube.com/watch\S*v=|youtu.be/)([\w-]+)')

def initModule(cod):
    cod.s2scommands["PRIVMSG"].append(youtubeLookup)
    cod.addBotCommand("YT", youtubeSearch)

def destroyModule(cod):
    cod.s2scommands["PRIVMSG"].remove(youtubeLookup)
    cod.delBotCommand("YT")

def rehash():
    pass

def youtubeLookup(cod, line):
    global YOUTUBE_REGEX

    if line.args[0] not in cod.channels:
        return

    chatline = line.args[-1]

    if "youtube" not in chatline:
        return

    videoid = None

    try:
        videoid = YOUTUBE_REGEX.split(chatline)[2]
    except:
        return

    try:
        info = requests.get("http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=json" % videoid).json()

        string = "^ Youtube: %s" % info["entry"]["title"]["$t"].encode("ascii", "replace")

        cod.privmsg(line.args[0], string)
    except Exception as e:
        cod.privmsg(line.args[0], "There was some error looking up that video: %s" % e.message)

def youtubeSearch(cod, line, splitline, source, destination):
    "Params: string to query youtube for"

    if len(splitline) < 2:
        cod.reply(source, destination, "Params: string to query youtube for")
        return

    search = " ".join(splitline[1:])

    try:
        info = requests.get("https://gdata.youtube.com/feeds/api/videos?q=%s&v=2&alt=jsonc" % search).json()

        video = info["data"]["items"][0]

        string = "Youtube: %s - http://youtu.be/%s" % (video["title"], video["id"])

        cod.reply(source, destination, string)

    except Exception as e:
        cod.reply(source, destination, "There was some error looking up that video: %s" % e.message)

