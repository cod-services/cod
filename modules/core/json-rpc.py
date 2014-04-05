import cherrypy
import json

from structures import makeClient
from web import RootPage

def initModule(cod):
    cod.webapp.root.add_page("json", JsonAPI)

def destroyModule(cod):
    cod.webapp.root.del_page("json")

class JsonAPI(RootPage):
    def __init__(self, cod):
        self.cod = cod

    @cherrypy.expose
    def command(self, cmd, *args):
        cherrypy.response.headers['Content-Type'] = 'application/json'

        cmd = str(cmd)
        source = make_smurf()
        destination = "<json-rpc>"
        line = cmd.upper() + " " + " ".join(args)
        splitline = args

        print line, splitline

        output = None

        if cmd in self.cod.botcommands:
            for impl in self.cod.botcommands[cmd]:
                output = impl(self.cod, line, splitline, source, destination)
                return format_reply(output)
        else:
            return format_reply("No such command", True)

        print output

    @cherrypy.expose
    def clientinfo(self):
        cherrypy.response.headers['Content-Type'] = 'application/json'

        clients = []

        for client in self.cod.clients.itervalues():
            clients.append(json.loads(client.json()))

        return format_reply(clients)

    @cherrypy.expose
    def chaninfo(self, channel=None):
        cherrypy.response.headers['Content-Type'] = 'application/json'

        if channel == None:
            channels = []

            for channel in self.cod.channels.itervalues():
                channels.append(json.loads(channel.json()))

            return format_reply(channels)

        else:
            channel = "#" + channel

            return format_reply(json.loads(self.cod.channels[channel].json()))

def make_smurf():
    return makeClient("<json-rpc>", "*false*", "Fake!uSer@LOLOL", "Json-RPC", "000000000")

def format_reply(output, error=False):
    toSend = {}
    if error:
        toSend["status"] = "error"
    else:
        toSend["status"] = "okay"

    toSend["output"] = output

    return json.dumps(toSend)

