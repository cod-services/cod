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

from textwrap import wrap

class TS6ServerConn():
    """
    Manages a TS6-like connection commands
    """

    def __init__(self, cod):
        self.umodes = "+Sio"

        self.cod = cod

        self.last_uid = 60466176 # 100000 in base 36
        self.numeric = cod.sid

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

        client.modes = self.umodes

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

        if len(message) > 450:
            lines = wrap(message, 450)
        else:
            lines = [message]

        for thatline in lines:
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

class InspircdServerConn(TS6ServerConn):
    def __init__(self, cod):
        TS6ServerConn.__init__(self, cod)
        self.umodes = "+iok"

    def join_client(self, client, channel):
        self.send_line(":%s FJOIN %s %s + :,%s" % (self.numeric, channel.name,
            channel.ts, client.uid))

    def add_metadata(self, client, key, value=""):
        self.send_line_sname("METADATA %s %s :%s" % (client.uid, key, value))

    def add_client(self, client):
        client.modes = self.umodes

        self.send_line_sname("UID %s %d %s 127.0.0.1 %s %s 127.0.0.1 %d +kio :%s" %
                (client.uid, int(time.time()), client.nick, client.host,
                    client.user, int(time.time()), client.gecos))
        self.send_line(":%s OPERTYPE Services" % client.uid)

class P10ServerConn():
    """
    This class translates actions and structures into P10 lines and the inverse.
    """

    def __init__(self, cod):
        """
        Initializes what is needed for a P10 connection.
        """

        self.umodes = "+iko"

        self.cod = cod

        self.last_uid = 0
        self.numeric = self.cod.sid

    def gen_uid(self):
        "Generates the next available UID"
        uid = base36encode(self.last_uid, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz[]")
        self.last_uid = self.last_uid + 1

        return self.numeric + uid

    def send_line(self, line):
        "Send a line to the server raw"

        self.cod.sendLine(line)

    def send_line_sname(self, line):
        "Send a line to the server prefixed with the server numeric"

        self.send_line("%s %s" % (self.numeric, line))

    def end_burst(self):
        "Signals the end of burst"

        self.send_line_sname("EB")

    def add_client(self, client):
        """
        Bursts a client to the P10 network.
        """

        now = int(time.time())

        client.modes = self.umodes

        self.send_line("%s N %s 1 %d %s %s +iko ]]]]]] %s :%s" %\
                (self.config["numeric"], client.nick, now, client.user,
                    client.host, client.uid, client.gecos))

    def quit(self, client, reason):
        """
        Sends a quit line to the P10 network.
        """

        self.send_line("%s Q :%s" % (client.uid, reason))

    def change_nick(self, client, nick):
        "Changes a local client's nickname"

        now = int(time.time())
        self.send_line("%s N %s :%d" % (self.numeric, nick, now))

    def _msg_like(self, type, client, target, message):
        "Generic wrapper for PRIVMSG and NOTICE line sending."

        self.send_line("%s %s %s :%s" % (client.uid, type, target, message))

    def privmsg(self, client, target, message):
        "Sends a PRIVMSG to a remote client."

        self._msg_like("P", client, target, message)

    def notice(self, client, target, message):
        "Sends a NOTICE to a remote client."

        self._msg_like("O", client, target, message)

    def join_client(self, client, channel):
        self.send_line("%s J %s %s" % (client.uid, channel.name, channel.ts))

    def part_client(self, client, channel, reason):
        self.send_line("%s L %s :%s" % (client.uid, channel.name, reason))

    def kill(self, killer, target, reason):
        "Remotely kills a client off a P10 network."

        self.send_line("%s D %s :%s!%s (%s)" %\
                (killer.uid, target.uid, killer.host, killer.nick, reason))

    def snote(self, line, mask="d"):
        #P10 does not support remote server notices
        pass

    def add_metadata(self, client, key, value=""):
        #P10 does not support client/channel metadata
        pass

