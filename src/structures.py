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

class Client():
    """
    Client data structure. Manages data for a client.
    """
    def __init__(self, nick, uid, ts, modes, user, host, ip, login, gecos):
        """
        Inputs: nickname, TS6 UID, Timestamp, user modes, user name, hostname,
        IP address, account the user is logged into with services, real name of
        user

        Creates client data structure
        """
        self.nick = nick
        self.uid = uid
        self.ts = ts
        self.modes = modes
        self.user = user
        self.host = host
        self.ip = ip
        self.login = login
        self.gecos = gecos
        self.sid = self.uid[:3]
        self.channels = []

        self.isOper = self.modes.find("o") != -1

    def __str__(self):
        """
        Output : nick!user@host: real name
        """
        return "%s!%s@%s :%s" % (self.nick, self.user, self.host, self.gecos)

    def privmsg(self, target, message):
        """
        Input: destination of message, message to send
        """
        return ":%s PRIVMSG %s :%s" % (self.uid, target, message)

    def notice(self, target, message):
        """
        Input: destination of message, message to send
        """
        return ":%s NOTICE %s :%s" % (self.uid, target, message)

    def quit(self):
        """
        Output: Quit message
        """
        return ":%s QUIT :Service unloaded" % self.uid

    def join(self, channel, op=False):
        """
        Input:  channel data structure, channel op status
        Output: valid s2s command for joining the channel
        """
        uid = self.uid

        if op:
            uid = "@" + uid

        return "SJOIN %s %s + %s" % (channel.ts, channel.name, uid)

    def burst(self):
        """
        Output: valid UID string to burst client onto the network
        """
        return ":%s UID %s 0 0 %s %s %s 0 %s :%s" % (self.sid, self.nick, self.modes, self.user, self.host, self.uid, self.gecos)

def makeService(nick, user, host, name, uid):
    """
    Inputs: nick, user, host, real name, TS6 UID

    Creates a services client.
    """
    return Client(nick, uid, "0", "+Sio", user, host, "*", nick, name)

def makeClient(nick, user, host, name, uid):
    """
    Inputs: nick, user, host, real name, TS6 UID

    Creates a generic client.
    """
    return Client(nick, uid, "0", "+Si", user, host, "*", nick, name)


class Channel():
    """
    Channel data structure
    """
    def __init__(self, name, ts):
        """
        Inputs: Name of channel, channel timestamp

        Creates a new channel structure.
        """
        self.name = name
        self.ts = ts
        self.clients = {}
        self.lists = {'b': [], 'e': [], 'I': [], 'q': []}
        self.modes = ""

    def listAdd(self, chanlist, mask):
        self.lists[chanlist].append(mask)

    def clientAdd(self, client, prefix = ""):
        self.clients[client.uid] = ChanUser(client)

class ChanUser():
    """
    Stub channel user structure for prefix tracking
    """
    def __init__(self, client, prefix = ""):
        self.client = client
        self.prefix = prefix

class Server():
    """
    Information on servers goes here
    """
    def __init__(self, sid, name, hops, realname):
        self.sid = sid
        self.name = name
        self.hops = hops
        self.realname = realname

