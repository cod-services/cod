class Client():
    def __init__(self, nick, uid, ts, modes, user, host, ip, login, gecos):
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

        self.isOper = self.modes.find("o") != -1

    def __str__(self):
        return "%s!%s@%s :%s" % (self.nick, self.user, self.host, self.gecos)

    def privmsg(self, target, message):
        return ":%s PRIVMSG %s :%s" % (self.uid, target, message)

    def notice(self, target, message):
        return ":%s NOTICE %s :%s" % (self.uid, target, message)

    def kill(self, target, msg):
        # Delete user from memory somehow
        return ":%s KILL %s" % (self.uid, target)

    def join(self, channel, op=False):
        uid = self.uid

        if op:
            uid = "@" + uid

        return "SJOIN %s %s + %s" % (channel.ts, channel.name, uid)

    def burst(self):
        return ":%s UID %s 0 0 %s %s %s 0 %s :%s" % (self.sid, self.nick, self.modes, self.user, self.host, self.uid, self.gecos)

def makeService(nick, user, host, name, uid):
    return Client(nick, uid, "0", "+Sio", user, host, "*", "*", name)

class Channel():
    def __init__(self, name, ts, snoop = False):
        self.name = name
        self.ts = ts
        self.clients = []
        self.lists = {'b': [], 'e': [], 'I': [], 'q': []}

    def __str__(self):
        return "%s: %s" % (self.name, " ".join(["" + name.prefix + name.client.nick for name in self.clients]))

    def listAdd(self, chanlist, mask):
        self.lists[chanlist].append(mask)

    def clientAdd(self, client, prefix = ""):
        self.clients.append(ChanUser(client))

class ChanUser():
    def __init__(self, client, prefix = ""):
        self.client = client
        self.prefix = prefix
