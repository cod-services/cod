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

import socket
import time
from utils import *

NAME="FPD checker"
DESC="Checks a flash policy daemon"

def initModule(cod):
    cod.botcommands["FPDTEST"] = [fpdtestCMD]

def destroyModule(cod):
    del cod.botcommands["FPDTEST"]

def rehash():
    pass

def fpdtestCMD(cod, line, splitline, source, destination):
    if(failIfNotOper(cod, cod.client, cod.clients[source])):
        return

    if len(splitline) < 3:
        cod.reply(source, destination, "Usage: FPDTEST <server to test> <port>")
        return

    s = socket.socket()

    host, port = splitline[1], int(splitline[2])

    oldtime = time.time()

    try:
        s.connect((host, port))
        cod.log("Connected to %s:%d" % (host, port), "===")

        s.send("<policy-file-request />\0")

        for line in s.makefile("r"):
            cod.log("%s:%d -- %s" % (host, port, line), "FPD")

    except Exception as e:
        cod.reply(source, destination, e)
        return

    newtime = time.time()

    delta = newtime-oldtime

    cod.reply(source, destination, "FPD at %s:%d appears to be okay in %4.2f seconds" %
            (host, port, delta))

