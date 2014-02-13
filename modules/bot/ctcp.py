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

from time import time

NAME="CTCP Replies"
DESC="CTCP reply handlers"

def initModule(cod):
    cod.s2scommands["PRIVMSG"].append(ctcp_reply)

def destroyModule(cod):
    cod.s2scommands["PRIVMSG"].remove(ctcp_reply)

def rehash():
    pass

def ctcp_reply(cod, line):
    if line.args[-1] == "\x01VERSION\x01":
        cod.notice(line.source, "\x01Cod version %s running on %s\x01" %
                (cod.version, cod.config["uplink"]["protocol"]), cod.clients[line.args[0]])

