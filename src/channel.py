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

from modes import *

class ChanUser:
    """
    Wrapper class around Client for channel users
    """

    def __init__(self, client, channel, status=CHFL_PEON):
        self.client = client
        self.status = status
        self.channel = channel

    def add_mode(self, mode):
        """
        Adds a status mode to a ChanUser
        """

        add = True

        for char in mode:
            if char == "+":
                add = True

            elif char == "-":
                add = False

            elif char == "v":
                self.status = self.status | CHFL_VOICE if add \
                        else self.status & ~(CHFL_VOICE)

            elif char == "h":
                self.status = self.status | CHFL_HALFOP if add \
                        else self.status & ~(CHFL_HALFOP)

            elif char == "o":
                self.status = self.status | CHFL_CHANOP if add \
                        else self.status & ~(CHFL_CHANOP)

            elif char == "a":
                self.status = self.status | CHFL_ADMIN if add \
                        else self.status & ~(CHFL_ADMIN)

            elif char == "y":
                self.status = self.status | CHFL_OWNER if add \
                        else self.status & ~(CHFL_OWNER)

    def add_prefix(self, prefix):
        for char in prefix:
            if char in PREFIXES:
                self.status = self.status | PREFIXES[char]

    def to_prefix(self):
        ret = ""

        if self.status & CHFL_VOICE:
            ret = "+" + ret

        if self.status & CHFL_HALFOP:
            ret = "%" + ret

        if self.status & CHFL_CHANOP:
            ret = "@" + ret

        if self.status & CHFL_ADMIN:
            ret = "!" + ret

        if self.status & CHFL_OWNER:
            ret = "~" + ret

        return ret

    def to_status(self):
        ret = ""

        for status in STATUSES:
            if self.status & status == status:
                ret += STATUSES[status] + " "

        ret = ret[:-1]

class Ban:
    """
    Ban structure
    """

    def __init__(self, mask, ts=None, setter=None, reason=None):
        self.mask = mask
        self.ts = int(time.time()) if ts == None else ts

        if setter is None:
            self.setter = "A.TS6.server"
        else:
            self.setter = setter.account if setter.account != "*" else setter.nick

        self.reason = reason if reason else "No reason given"

class Channel:
    """
    Channel structure
    """

    def __init__(self, name, ts=None):
        new = ts == None #if we are making a new channel

        self.name = name
        self.ts = int(ts) if ts != None else int(time.time())

        self.clients = {}
        self.metadata = {}

        self.lists = {
                LIST_BAN:    CaseInsensitiveDict(),
                LIST_QUIET:  CaseInsensitiveDict(),
                LIST_EXCEPT: CaseInsensitiveDict(),
                LIST_INVEX:  CaseInsensitiveDict(),
        }

        self.limit = None
        self.key = None
        self.throttle = None
        self.properties = PROP_NONE

    def add_member(self, client, prefix=None):
        uid = client.uid
        cuser = ChanUser(client, self)

        if prefix != None:
            cuser.add_prefix(prefix)

        client.channels.append(cuser)

        self.clients[client.uid] = cuser

    def del_member(self, client, reason=None):
        del self.clients[client.uid]
        client.client.channels.remove(self.name)
        del client

    def check_banned(self, client):
        return False

    def add_ban(self, ban_type, ban):
        if ban.mask not in self.lists[ban_type]:
            self.lists[ban_type][ban.mask] = ban

    def del_ban(self, ban_type, mask):
        if mask in self.lists[ban_type]:
            del self.lists[ban_type][mask]

    def add_prop_by_letter(self, direction, flag):
        flag = CHANMODES[3][flag]

        self.properties = self.properties | flag if direction \
                else self.properties & ~(flag)

    def prop_string(self):
        ret = ""

        for prop in PROPS:
            if self.properties & prop == prop:
                ret += PROPS[prop] + " "

        return ret[:-1]

