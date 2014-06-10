"""
Copyright (c) 2013-4: Sam Dodrill, Jessica Williams
All rights reserved.

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anypony to use this software for any purpose,
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

This code was originally written for eon, but has been ported to cod.
"""

from sprunge import sprunge
from textwrap import wrap
from niilib.b36 import *
import time

class TS6ServerConn():
    """
    Manages a TS6-like connection commands
    """

    def __init__(self, cod):
        self.umodes = "+Si"

        self.cod = cod

        self.last_uid = 60466176 # 100000 in base 36
        self.numeric = cod.sid

        self.p10 = False

    def gen_uid(self):
        uid = base36encode(self.last_uid)

        self.last_uid = self.last_uid + 1

        return self.numeric + uid

    def send_line(self, line):
        self.cod.sendLine(line)

    def send_line_sname(self, line):
        self.send_line(":%s %s" % (self.numeric, line))

    def add_client(self, client):
        now = int(time.time())

        self.send_line_sname("EUID %s 1 %d %s %s %s 0 %s * * :%s" %\
                (client.nick, now, client.modes, client.user, client.host,
                    client.uid, client.gecos))

    def quit(self, client, reason):
        self.send_line(":%s QUIT :%s" % (client.uid, reason))

    def change_nick(self, client, nick):
        now = int(time.time())

        self.send_line(":%s NICK %s :%d" % (client.uid, nick, now))

    def _msg_like(self, type, client, target, message):
        lines = []

        if len(message) > 400:
            lines = wrap(message, 400)
        else:
            lines = [message]

        if len(lines) > 5:
            self.send_line(":%s %s %s :Output too big: %s" %
                    (client.uid, type, target, sprunge(message)))
            return

        for thatline in lines:
            thatline = " " if thatline == "" else thatline
            self.send_line(":%s %s %s :%s" %
                    (client.uid, type, target, thatline))

    def privmsg(self, client, target, message):
        self._msg_like("PRIVMSG", client, target, message)

    def notice(self, client, target, message):
        self._msg_like("NOTICE", client, target, message)

    def join_client(self, client, channel):
        self.send_line(":%s JOIN %s %s +" %\
                (client.uid, channel.ts, channel.name))

    def part_client(self, client, channel, reason):
        self.send_line(":%s PART %s" %\
                (client.uid, channel.name))

    def kill(self, killer, target, reason):
        self.send_line(":%s KILL %s :spacing %s" %\
                (killer.uid, target.uid, reason))

    def snote(self, line, mask="d"):
        self.send_line_sname("ENCAP * SNOTE %s :%s" % \
                (mask, line))

    def add_metadata(self, client, key, value):
        self.send_line_sname("ENCAP * METADATA ADD %s %s :%s" %
                (client.uid, key.upper(), value))

