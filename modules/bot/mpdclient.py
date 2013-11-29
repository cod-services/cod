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

from mpd import MPDClient, ConnectionError
from utils import *

NAME="MPD Client"
DESC="Does simple lookups and status on an mpd server"

global mpd

mpd = MPDClient()

def initModule(cod):
    global mpd

    cod.log("Establishing connection to MPD server", "===")

    mpd = MPDClient(use_unicode=True)
    mpd.timeout = 10
    mpd.idletimeout = None
    mpd.connect(cod.config["mpd"]["host"], cod.config["mpd"]["port"])

    cod.log("done", "===")

    cod.botcommands["MPD"] = [commandMPD]

def destroyModule(cod):
    global mpd

    cod.log("Disconnecting from MPD server", "===")

    try:
        mpd.close()
        mpd.disconnect()
    except ConnectionError as e:
        pass

    del cod.botcommands["MPD"]
    del mpd

def commandMPD(cod, line, splitline, source, destination):
    global mpd

    try:
        mpd.currentsong()
    except:
        cod.log("===", "Reconnecting to MPD server")
        mpd.close()
        mpd.disconnect()
        mpd.connect(cod.config["mpd"]["host"], cod.config["mpd"]["port"])

    if len(splitline) < 2:
        mpd.update()
        cur = mpd.currentsong()

        cod.reply(source, destination, "Now playing: %s -- %s" % \
                (cur["artist"], cur["title"]))
        return

    if splitline[1].upper() == "FIND":
        query = " ".join(splitline[2:])

        cod.reply(source, destination, "Searching for %s" % query)

        results = mpd.find("any", query)

        client = cod.clients[source]

        for result in results:
            cod.notice(source, "%s -- %s" % \
                    (result["artist"], result["title"]))

    if failIfNotOper(cod, cod.client, cod.clients[source]):
        return

    if splitline[1].upper() == "NEXT":
        mpd.next()

        cod.reply(source, destination, "Next song is playing")

    elif splitline[1].upper() == "PREV":
        mpd.previous()

        cod.privmsg(destination, "Previous song is playing")

    elif splitline[1].upper() == "PAUSE":
        mpd.pause()

        cod.reply(source, destination, "Paused")

    elif splitline[1].upper() == "PLAY":
        if len(splitline) < 3:
            mpd.play()
            cod.reply(source, destination, "Playing")
        else:
            mpd.play(splitline[2])

    elif splitline[1].upper() == "LISTSTATUS":
        mpd.update()
        mpd.iterate = True

        cur = mpd.currentsong()

        for line in mpd.playlistinfo():
            cod.notice(source, "%s%s: %s" % \
                    (("* " if cur["id"] == line["id"] else "  "),
                        line["artist"], line["title"]))

