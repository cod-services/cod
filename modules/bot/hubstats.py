"""
Copyright (c) 2014, Christine Dodrill
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

NAME="Github statistics"
DESC="Shows Github statistics via the Open Source Report Card"

def initModule(cod):
    cod.addBotCommand("OSRC", personCheck)

def destroyModule(cod):
    cod.delBotCommand("OSRC")

def rehash():
    pass

def personCheck(cod, line, splitline, source, destination):
    "ARGS: <person> - looks up <person> on http://osrc.dfm.io/ and summarizes their report card"

    if len(splitline) < 2:
        cod.reply(source, destination, personCheck.__doc__)

    person = splitline[1]

    try:
        info = requests.get("http://osrc.dfm.io/%s.json" % person).json()

        toplang = info["usage"]["languages"][0]
        toprepo = info["repositories"][0]

        string = "%s: %s user (top %d%%) - Top repo: %s (%d events)" %\
                (info["name"], toplang["language"], toplang["quantile"],
                        toprepo["repo"], toprepo["count"])

        return string
    except Exception as e:
        return "There was some error looking that person up: %s" % e.message

