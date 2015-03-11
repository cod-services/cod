# Copyright (C) 2014 Christine Dodrill <shadow.h511@gmail.com> All rights reserved.
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

NAME="channel info"
DESC="Shows detailed channel information"

def initModule(cod):
    cod.addBotCommand("INFO", cmdINFO, True)

def destroyModule(cod):
    cod.delBotCommand("MEM")

def rehash():
    pass

def cmdINFO(cod, line, splitline, source, destination):
    "Shows channel information for curious opers"

    channel = cod.channels[splitline[1]]

    ret = []

    ret.append("INFO on %s" % channel.name)

    for uid, cuser in channel.clients.iteritems():
        client = cuser.client
        status = cuser.to_status()
        prefix = cuser.to_prefix()

        ret.append("%s: (%s@%s) [%s] [%s] [%s] %s(%s)" %\
                (client.nick, client.user, client.host, client.ip, client.gecos,
                    client.login, status, prefix))

    ret.append("Modes: %s" % (channel.prop_string()))

    for kind, banlist in channel.lists.iteritems():
        for mask, ban in banlist.iteritems():
            ret.append("%s %s" % (kind, ban.mask))

    cod.notice(source, "\n".join(ret))

    cod.servicesLog("%s: INFO %s" % (source.nick, channel.name))

