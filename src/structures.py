"""
Copyright (c) 2013, Christine Dodrill
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

import time

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

        #Okay python you win
        self.client = self

        self.name = self.nick

        self.isOper = self.modes.find("o") != -1

        if self.modes.find("S") != -1:
            self.isOper = False

    def __str__(self):
        """
        Output : Client UID
        """
        return self.uid

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
        Input:  channel data structure
        Output: valid s2s command for joining the channel
        """
        uid = self.uid

        return ":%s JOIN %s %s +" % (uid, channel.ts, channel.name)

    def burst(self):
        """
        Output: valid UID string to burst client onto the network
        """
        return ":%s EUID %s 1 %d %s %s %s 0 %s * * :%s" %\
                (self.sid, self.nick, int(time.time()), self.modes, self.user,
                        self.host, self.uid, self.gecos)

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
        self.msgbuffer = []

    def __str__(self):
        return self.name

    def listAdd(self, chanlist, mask):
        self.lists[chanlist].append(mask)

    def clientAdd(self, client, prefix=""):
        matching = filter((lambda x: x == client.uid), self.clients)

        if len(matching) == 0:
            self.clients[client.uid] = ChanUser(client, prefix)

        client.channels.append(self)

class ChanUser():
    """
    Stub channel user structure for prefix tracking
    """
    def __init__(self, client, prefix=""):
        self.client = client
        self.prefix = prefix

class Server():
    """
    Information on servers goes here
    """

    def __init__(self, sid, name=None, hops=None, realname=None):
        self.sid = sid
        self.name = name
        self.hops = hops
        self.realname = realname
        self.clients = []

