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

def initModule(cod):
    cod.s2scommands["NICK"].append(remindAway)

def destroyModule(cod):
    cod.s2scommands["NICK"].remove(remindAway)

def rehash():
    pass

def remindAway(cod, line):
    if line.args[0].endswith("|away"):
        cod.sendLine(":%s NOTICE %s :You are making your away status known by nickname change" %\
                (cod.client.uid, line.source))
        cod.sendLine(":%s NOTICE %s :Please see /quote HELP AWAY for more information on a better system" %\
                (cod.client.uid, line.source))

