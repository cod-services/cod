# Copyright (C) 2014 Sam Dodrill <shadow.h511@gmail.com> All rights reserved.
#
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
#
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
#
# 3. This notice may not be removed or altered from any source
#    distribution.
#

from fnmatch import fnmatch

NAME="channel info"
DESC="Shows detailed channel information"

def initModule(cod):
    cod.addBotCommand("CHECKBANS", cmdCHECKBANS, True)

def destroyModule(cod):
    cod.delBotCommand("CHECKBANS")

def rehash():
    pass

def cmdCHECKBANS(cod, line, splitline, source, destination):
    "Checks every channel on the network for a ban"

    ban = splitline[1].lower()

    ret = []

    ret.append("Bans for %s" % ban)

    for name, channel in cod.channels.iteritems():
        for kind, banlist in channel.lists.iteritems():
            for mask, banobj in banlist.iteritems():
                mask = mask.replace("*", "").lower()
                if fnmatch(mask, ban):
                    ret.append("%s in %s by %s on %s" % (kind, name, banobj.setter, banobj.ts))

    cod.notice(source, "\n".join(ret))

    cod.servicesLog("%s: CHECKBANS %s" % (source.nick, ban))

