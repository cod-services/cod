#!/usr/bin/python

"""
Copyright (c) 2013-2014, Sam Dodrill
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

VERSION = "0.3"

from niilib import config
from niilib import log
from ircmess import IRCLine
from niilib.b36 import *
from select import select
from textwrap import wrap

import atheme
import socket
import os
import sys
import ssl
import gc
import sqlite3 as lite
import traceback

from structures import *
from utils import *


class Cod():

    def __init__(self, configpath):
        """
        The main Cod class. This holds all the data structures needed
        for Cod to function. The socket, command tables, server data,
        client tables, and other variables needed for Cod to work
        properly are initialized here.
        """

        self.link = socket.socket()

        self.clients = {}
        self.channels = {}
        self.servers = {}
        self.modules = {}
        self.hooks = {}

        self.socks = [self.link]
        self.sockhandlers = {self.link: self.process}

        self.lastid = 60466176 # 100000 in base 36

        self.loginFunc = None

        self.s2scommands = {"PRIVMSG": []}
        self.botcommands = {}
        self.opercommands = {}

        self.bursted = False
        self.db = None
        self.protocol = None
        self.sid = ""

        #Load config file
        self.config = config.Config(configpath).config

        self.version = "%s-%s" % (VERSION, self.config["me"]["netname"])

        #logger instance
        self.logger = log.Logger(self.config["etc"]["logfile"])

        #Fork to background if needed
        if self.config["etc"]["production"]:
            self.log("Forking to background")

            try:
                pid = os.fork()
            except OSError, e:
                raise Exception, "%s [%d]" % (e.strerror, e.errno)

            if (pid == 0):
                os.setsid()
            else:
                os._exit(0)

        if self.config["uplink"]["ssl"]:
            self.link = ssl.wrap_socket(self.link)
            self.log("SSL enabled")

        self.log("Initializing Atheme XMLRPC connector")

        self.services = atheme.CodAthemeConnector(self)

        #pid value
        self.pid = os.getpid()

        self.log("Initializing Database")

        self.db = lite.connect(self.config["me"]["dbpath"])
        cur = self.db.cursor()

        try:
            cur.execute("PRAGMA table_info(Thistabledoesnotexist);")
            rows = cur.fetchall()

        except lite.DatabaseError as e:
            self.log("Database at %s unreadable" %
                    self.config["me"]["dbpath"], "!!!")
            print e
            sys.exit(-1)

        self.log("done")

        self.log("Establishing connection to uplink")

        self.link.connect((self.config["uplink"]["host"],
            self.config["uplink"]["port"]))

        self.log("done")

        self.sid = self.getSID()

        self.log("SID is %s" % self.sid)

        self.log("Loading %s protocol module" %
                self.config["uplink"]["protocol"])

        self.loadmod(self.config["uplink"]["protocol"])

        self.log("Sending credentials to remote IRC server")

        self.loginFunc(self)

        self.log("done")

        if "web" in self.config:
            self.log("Loading web frontend")

            self.loadmod("webapp")

            self.log("done")

        self.log("Creating and bursting client")

        self.client = makeService(self.config["me"]["nick"],
                self.config["me"]["user"], self.config["me"]["host"],
                self.config["me"]["desc"], self.getUID())

        self.clients[self.client.uid] = self.client

        self.burstClient(self, self.client)

        self.log("done")

        #Inform operators that Cod is initialized
        self.log("Cod initialized", "!!!")

    def getUID(self, sid=None):
        """
        Returns a valid, unique TS6 UID for use with services clients
        """

        if sid == None:
            sid = self.sid

        ret = self.lastid
        self.lastid = self.lastid + 1

        return sid + base36encode(ret)

    def getSID(self, string=None):
        """
        Returns a server ID number based on the string provided, default is
        the configured server name and description, much like how inpsircd
        does SID generation.
        """

        if string is None:
            string = self.config["me"]["name"] + self.config["me"]["desc"]

        hashval = 1
        for char in string:
            char = ord(char)
            hashval = hashval * (char * (char + 1))

        return str(hashval)[:3]

    def loadmod(self, modname):
        """
        Input: module name

        This function tries to load a module and initialize its commands to
        the bot or s2s command tables. This function does no error checking and
        it is up to functions calling this to do so.
        """

        if modname in self.modules:
            return

        oldpath = list(sys.path)
        sys.path.insert(0, "modules/")
        sys.path.insert(1, "modules/protocol")
        sys.path.insert(2, "modules/core")
        sys.path.insert(3, "modules/experimental")
        sys.path.insert(4, "modules/bot")
        sys.path.insert(5, "modules/services")
        sys.path.insert(6, "modules/announcer")
        sys.path.insert(7, "modules/scrapers")

        if self.config["etc"]["contrib"]:
            sys.path.insert(8, "modules/contrib")

        self.modules[modname] = __import__(modname)
        self.modules[modname].initModule(self)
        self.log("Module %s loaded" % modname)

        sys.path[:] = oldpath

    def unloadmod(self, modname):
        """
        Input: module name

        This function tries to unload a module and destroy its commands to the
        bot or s2s command tables as makes sense. This function does not error
        checking and it is up to functions calling this to do so.
        """

        self.modules[modname].destroyModule(self)
        del self.modules[modname]
        del sys.modules[modname]

        #Run the garbage collector
        gc.collect()

        self.log("Module %s unloaded" % modname)

    def addBotCommand(self, command, func, oper=False):
        """
        Adds a botcommand to the bot commands table, optionally adding it
        to the special table full of oper-only commands.
        """

        wheretoadd = self.botcommands

        if oper:
            wheretoadd = self.opercommands
            self.log("%s added as OPERCOMMAND" % command, "CMD")
        else:
            self.log("%s added as USERCOMMAND" % command, "CMD")

        wheretoadd[command] = [func]

    def delBotCommand(self, command):
        """
        Removes a bot command from the oper-only and normal user level bot commands
        tables if applicable
        """

        try:
            del self.botcommands[command]
            self.log("%s deleted as USERCOMMAND" % command, "CMD")
        except KeyError:
            del self.opercommands[command]
            self.log("%s deleted as OPERCOMMAND" % command, "CMD")

    def addHook(self, name, func):
        """
        Adds a hook to the hook table.
        """

        if name not in self.hooks:
            self.hooks[name] = []

        self.hooks[name].append(func)

    def delHook(self, name, func):
        """
        Deletes a hook from the hook table.
        """

        self.hooks[name].remove(func)

    def runHooks(self, name, args):
        """
        Runs a hook with arguments passed through. Be sure the argument types
        match up or weird things may happen.
        """

        if name not in self.hooks:
            return

        for func in self.hooks[name]:
            try:
                func(self, *args)
            except Exception as e:
                cod.servicesLog("%s %s" % (type(e), e.message))

    def rehash(self):
        """
        Input: none

        This function rehashes the configuration in memory with the
        configuration on the disk.
        """
        self.log("Rehashing...")

        self.servicesLog("Rehashing config file.")

        self.config = config.Config("config.json").config

        for module in self.modules:
            #cod.log("Rehashing %s" % module, "===")
            try:
                self.modules[module].rehash()
            except:
                pass

        self.log("Rehash complete")

    def sendLine(self, line):
        """
        Input: line to send to ircd

        This function will send a line to the upstream ircd. This does no
        checking and will print the line if the program is in debug mode.
        """
        if self.config["etc"]["debug"]:
            self.log(line, ">>>")

        # Check for \r\n in message, closes issue #17
        if "\r" in line:
            "".join(line.split("\r"))

        if "\n" in line:
            "".join(line.split("\n"))

        self.link.send("%s\r\n" % line)

    def privmsg(self, target, line, source=None):
        """
        Input: target of message (UID or channel), message to send, source of
        message (default Cod's main client UID)

        A nice macro around PRIVMSG for convenience. Allows for changing the
        source of the message.
        """

        if source is None:
            source = self.client

        self.protocol.privmsg(source, target, line)

    def notice(self, target, line, source=None):
        """
        Input: target of message (UID or channel), message to send, source of
        message (default Cod's main client UID)

        A nice macro around NOTICE for convenience.Allows for changing the
        source of the message.
        """

        if source is None:
            source = self.client

        self.protocol.notice(source, target, line)

    def kill(self, target, source=None, message="Connection has been terminated."):
        """
        Wrapper function to kill off clients and remove their client data
        """

        if source is None:
            source = self.client

        self.protocol.kill(source, target, message)

        self.clients.pop(target.uid)

    def join(self, channel, client=None):
        """
        Input: channel to join, client to join to the channel (default Cod
        internal client)

        This is a convenience macro around SJOIN (which requires a matching TS)
        to join a channel. Will also let you join another client Cod controls to
        a channel. Also lets you set channel op on join.
        """

        if client is None:
            client = self.client

        if channel not in self.channels:
            self.channels[channel] = Channel(channel, int(time.time()))

        channel = self.channels[channel]

        self.protocol.join_client(client, channel)

        client.channels.append(channel.name)

    def part(self, channel, message="Leaving", client=None):
        """
        Input: channel to part, client to part from the channel (default Cod
        internal client), part message
        """

        if client is None:
            client = self.client

        channel = self.channels[channel]

        self.protocol.part_client(client, channel, message)

        client.channels.remove(channel.name)

    def kill_stale_references(self, client):
        client = cod.clients["%s" % client]

        for chname in self.channels:
            channel = self.channels[chname]

            murderlist = []

            for uid in channel.clients:
                cli = channel.clients[uid]
                if cli.client.uid == client.uid:
                    murderlist.append(uid)

            for uid in murderlist:
                del channel.clients[uid]

    def pop_empty_channels(self):
        """
        Remove information on any empty channels
        """

        murderlist = []

        for chname in self.channels:
            channel = self.channels[chname]

            if len(channel.clients) == 0 and "P" not in channel.modes:
                murderlist.append(channel)

        for victim in murderlist:
            del self.channels[victim.name]

    def snote(self, line, mask="d"):
        """
        Inputs: line to send, target server notice mask

        This function lets you send out a global server notice matching an
        arbitrary SNOMASK, but the default is the debug SNOMASK.
        """

        self.protocol.snote(line, mask)

    def log(self, message, prefix="---"):
        """
        Inputs: message to log, prefix to prepend to message (default "---")

        This function prints a message to the screen unless we are forked to
        the background (not checking that messes things up). If the prefix is
        the default prefix, it will also send out a debug snote with the log
        message.
        """
        if not self.config["etc"]["production"]:
            print prefix, message

        if self.bursted and prefix == "!!!":
            self.snote("%s" % (message))

        self.logger.log("%s %s" % (prefix, message))

    def servicesLog(self, line, client=None):
        """
        Inputs: line to log to services snoop channel

        This is a convenience function to send a message to the services logging
        channel. This channel is configurable in the config file.
        """

        if client is None:
            client = self.client

        self.privmsg(self.config["etc"]["snoopchan"], line, client)

        self.logger.log("SVS: %s: %s" % (client.nick, line))

    def findClientByNick(self, nick):
        """
        Inputs: nickname to find client data structure of

        This searches the Cod client table for a client matching a nick. If
        no matching client is found, None will be returned.
        """
        nick = nick.lower()

        for client in self.clients:
            if cod.clients[client].nick.lower() == nick:
                return cod.clients[client]

        return None

    def reply(self, source, destination, line):
        """
        Inputs: source of message, destination of message, line to send

        According to the IRC RFC's, bots should use NOTICEs whenever possible.
        This simplifies functions returning data to clients over PRIVMSG/NOTICE
        to call one function instead of choosing between two.
        """
        if source == destination:
            #PM
            cod.notice(destination, line)
        else:
            #Channel message
            cod.privmsg(destination, line)

    def go(self):
        """
        Cod's main function
        """

        self.buf = ""

        while True:
            try:
                inputready, outputready, execeptready = select(self.socks,[],[])

                for s in inputready:
                    self.sockhandlers[s]([cod, s])

            except KeyboardInterrupt:
                print " <-- Control-C pressed, dying"
                self.servicesLog("See you on the other side.")

                self.db.close()
                self.sendLine(self.client.quit())

                for module in self.modules:
                    if module == "elemental-ircd" or module == "inspircd":
                        continue
                    elif module == "admin":
                        continue
                    try:
                        self.modules[module].destroyModule(self)
                    except Exception:
                        print "Lol can't unload %s" % module

                self.sendLine("SQUIT :Killed.")

                os.system("kill -s SIGKILL %d" % self.pid)
                sys.exit(0)

        self.log("Oh, I am slain.")

    def process(self, args):
        tbuf = self.link.recv(2048)
        tbuf = self.buf + tbuf

        lines = tbuf.split("\n")

        self.buf = lines[-1]
        lines = lines[:-1]

        self.processLines(lines)

    def processLines(self, lines):
        """
        This checks and does all the module call handlers for lines from the
        upstream socket.
        """

        for line in lines:
            if len(line) == 0:
                continue

            if line[-1] == "\r":
                line = line[:-1]

            # Automatically make P10 protocols have their lines parsed
            # differently
            lineobj = IRCLine(line, self.protocol.p10)

            #debug output
            if self.config["etc"]["debug"]:
                self.log(line, "<<<")

            if lineobj.verb == "ERROR":
                #If ERROR is sent, it's already fatal.
                raise KeyboardInterrupt

            #Handle server commands
            try:
                for impl in self.s2scommands[lineobj.verb]:
                    try:
                        impl(cod, lineobj)
                    except KeyError as e:
                        continue
                    except Exception as e:
                        if not self.config["etc"]["production"]:
                            self.servicesLog("%s %s %s" %(type(e), e.message, lineobj))
                            traceback.print_exc(file=sys.stdout)
                        continue
            except KeyError:
                pass

if __name__ == "__main__":
    print "!!! Cod %s starting up" % VERSION

    cod = None

    if len(sys.argv) < 2:
        cod = Cod("config.json")
    else:
        cod = Cod(sys.argv[1])

    #start up

    cod.go()

