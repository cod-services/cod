NAME="PingServ"
DESC="IRC interface to NodePing"

from nodeping import *
from structures import makeService

global client

def initModule(cod):
    global client

    if "nodeping" not in cod.config:
        cod.serviceLog("Need nodeping config")
        raise ImportError

    client = makeService(cod.config["nodeping"]["nick"], cod.config["nodeping"]["user"],
            cod.config["nodeping"]["host"], cod.config["nodeping"]["gecos"],
            cod.getUID())

    cod.clients[client.uid] = client

    cod.protocol.add_client(client)
    cod.log("Bursted pingserv client")

    cod.join(cod.config["etc"]["snoopchan"], client)

    cod.addHook("privmsg", handle_commands)

def destroyModule(cod):
    global client

    cod.protocol.quit(client, "Service unloaded")
    del cod.clients[client.uid]

    cod.delHook("privmsg", handle_commands)

def rehash():
    pass

def handle_commands(cod, target, line):
    global client

    if target.uid != client.uid:
        return

    command = ""
    source = line.source
    userline = line.args[-1].split()

    command = userline[0].upper()

    if command == "UPTIME":
        np = NodePing(cod.config["nodeping"]["token"])

        checks = np.get_checks(cod.config["nodeping"]["filter"])

        for check in checks:
            name = check["label"]

            try:
                uptime = np.get_uptime(check)

                stats = uptime[-1]

                cod.notice(source, "%s: %s%% uptime" % (name, stats["uptime"]), client)
            except ValueError:
                cod.notice(source, "%s is too new to have uptime history" % name, client)

