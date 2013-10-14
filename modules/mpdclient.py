"""
Copyright (c) 2013, Sam Dodrill
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

  Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from mpd import MPDClient
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

    mpd.close()
    mpd.disconnect()

    del cod.botcommands["MPD"]
    del mpd

def commandMPD(cod, line, splitline, source, destination):
    global mpd

    if len(splitline) < 2:
        cod.reply(source, destination, "Not enough arguments")
        return

    if splitline[1].upper() == "FIND":
        query = " ".join(splitline[2:])

        cod.reply(source, destination, "Searching for %s" % query)

        results = mpd.find("any", query)

        client = cod.clients[source]

        for result in results:
            cod.notice(source, "%s -- %s" % \
                    (result["artist"], result["title"]))
    elif splitline[1].upper() == "STATUS":
        mpd.update()
        cur = mpd.currentsong()

        cod.reply(source, destination, "%s -- %s -- %4.2f%%" % \
                (cur["artist"], cur["title"], float(cur["pos"])/float(cur["time"])))

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
            cod.reply(source, destination, "%s%s: %s" % \
                    (("* " if cur["id"] == line["id"] else "  "),
                        line["artist"], line["title"]))

