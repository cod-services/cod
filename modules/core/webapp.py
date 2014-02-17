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

NAME="Web App"
DESC="A web frontend to Cod"

import cherrypy
import wsgiref.handlers
import json
import sys
import misaka

from threading import Thread
from cherrypy.process.plugins import Daemonizer

thread = None

def initModule(cod):
    global thread

    #cod.webappthread = RunThread(cod)
    #cod.webappthread.start()

    cherrypy.config.update({'server.socket_port': cod.config["web"]["port"],
        'server.socket_host': cod.config["web"]["bindhost"],
        'engine.autoreload_on': False})

    cod.webapp = WebAppHandler(cod)

def destroyModule(cod):
    cherrypy.server.stop()

class RunThread(Thread):
    def __init__(self, cod):
        Thread.__init__(self)
        self.cod = cod

    def run(self):
        self.cod.log("Started webserver", "WEB")
        self.webapp = WebAppHandler(self.cod)
        sys.exit(0)

class WebAppHandler(object):
    def __init__(self, cod):
        self.cod = cod

        self.mapper = cherrypy.dispatch.RoutesDispatcher()

        self.add_page("clientinfo", "/clientinfo", ClientInfo)
        self.add_page("hello", "/hello", HelloWorld)

        cherrypy.config.update({'server.socket_port': self.cod.config["web"]["port"],
            'server.socket_host': str(self.cod.config["web"]["bindhost"]),
            'engine.autoreload_on': False})

        cherrypy.engine.signals.subscribe()
        cherrypy.engine.start()

    def add_page(self, route, special, Controller):
        self.mapper.connect(route, special, controller=Controller(self.cod).index)

        print "adding", route, "as", special, "with", Controller

        cherrypy.tree.mount(None, config={"/": {"request.dispatch": self.mapper}})

class HelloWorld:
    def __init__(self, cod):
        self.cod = cod

    @cherrypy.expose
    def index(self):
        return "Hello world! Version %s" % self.cod.version

class ClientInfo(object):
    def __init__(self, cod):
        self.cod = cod

    def style(self):
        return """
        <style>
        table {
            border: 1;
        }
        </style>
        """

    def index(self):
        replies = []

        replies.append(self.style())

        replies.append("<center><h1>%s Network clients</h1></center>" % self.cod.config["me"]["netname"])

        replies.append("<table>")
        replies.append("<tr><td> Nick </td><td> User </td><td> Host </td><td> Gecos </td><td> Channels </td>\n")
        replies.append("</tr>")

        for uid in self.cod.clients:
            client = self.cod.clients[uid]

            try:
                replies.append("<tr><td> %s </td><td> %s </td><td> %s </td><td> %s </td><td> %s </td></tr>\n" %
                        (client.nick, client.user, client.host, client.gecos,
                            ", ".join([x.name for x in client.channels])))
            except AttributeError:
                pass

        replies.append("</table> <br />")

        replies.append("<table><tr><td> Channel name </td><td> Ops </td></tr>\n")

        for chname in self.cod.channels:
            channel = self.cod.channels[chname]

            ops = []

            for uid in channel.clients:
                chancli = channel.clients[uid]

                if "@" in chancli.prefix:
                    ops.append(chancli.client.nick)

            if ops == [] or len(channel.clients) == 0:
                continue

            replies.append("<tr><td> %s </td><td> %s </td></tr>\n" % (channel.name, " ".join(ops)))

        replies.append("</table> <br />")

        replies.append("<table><tr><td> Channel name </td><td> Modes </td><td> TS </td><td> Population </td><td> Nicks </td></tr>\n")

        for chname in self.cod.channels:
            channel = self.cod.channels[chname]

            nicks = []

            if len(channel.clients) == 0:
                continue

            for client in channel.clients:
                client = channel.clients[client].client

                if client.nick in nicks:
                    self.cod.servicesLog("Wtf: duplicate client %s" % client.nick)

                try:
                    nicks.append("%s%s" % (channel.clients[client].prefix, client.nick))
                except:
                    nicks.append(client.nick)

            replies.append("<tr><td> %s </td><td> %s </td><td> %s </td><td> %d </td><td> %s </td></tr>\n" %
                    (chname, channel.modes, channel.ts, len(nicks), " ".join(nicks)))

        replies.append("</table>")

        return replies
    index.exposed = True

