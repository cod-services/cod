import time

from xmlrpclib import ServerProxy, Fault


class Parent(object):
    def __init__(self, parent):
        self.parent = parent


class NickServ(Parent):
    def __init__(self, parent):
        self.parent = parent
        self.flags = ["Hold", "HideMail", "NeverOp", "NoOp", "NoMemo",
                      "EMailMemos", "Private"]

    def _parse_access(self, data):
        raw_lines = data.split("\n")

        list = []
        for line in raw_lines:
            fields = line.split(" ")

            if fields[0] != "Access":
                continue
            try:
                tuple = {"channel": fields[4], "flags": fields[2]}
            except:
                pass
            list.append(tuple)

        return list

    def list_own_access(self):
        return self._parse_access(self.parent.command("NickServ", "LISTCHANS"))

    def list_access(self, target):
        return self._parse_access(self.parent.command("NickServ", "LISTCHANS",
            target))

    def get_info(self, target):
        data = self.parent.command("NickServ", "INFO", target)
        raw_lines = data.split("\n")

        tuple = {}
        for line in raw_lines:
            if "Information on" in line:
                continue
            if ":" not in line:
                continue

            fields = line.split(":", 1)
            try:
                tuple[fields[0].strip()] = fields[1].strip()
            except:
                pass

        return tuple

    def get_account_flags(self, target):
        data = self.get_info(target)
        flags = data["Flags"]

        tuple = {}
        for flag in self.flags:
            if flag in flags:
                tuple[flag] = True
            else:
                tuple[flag] = False

        return tuple

    def set_password(self, password):
        self.parent.command("NickServ", "SET", "PASSWORD", password)

    def set_email(self, email):
        self.parent.command("NickServ", "SET", "EMAIL", email)


class ChanServ(Parent):
    """
    Parse Atheme ChanServ responses.  Since the XML interface provides the same output as the IRC interface, we
    have to do this.  It"s kind of a pain in the ass.
    """
    def __init__(self, parent):
        self.parent = parent
        self.flags = ["HOLD", "SECURE", "VERBOSE", "VERBOSE_OPS", "RESTRICTED",
                "KEEPTOPIC", "TOPICLOCK", "GUARD", "FANTASY", "PRIVATE",
                "LIMITFLAGS"]

    def kick(self, channel, victim, reason):
        self.parent.command("ChanServ", "KICK", channel, victim, reason)

    def get_access_list(self, channel):
        data = self.parent.command("ChanServ", "FLAGS", channel)
        raw_lines = data.split("\n")

        list = []
        for line in raw_lines:
            tuple = {}

            try:
                data = line.split(None, 3)
                tuple["id"] = int(data[0])
                tuple["nick"] = data[1]
                tuple["flags"] = data[2]
                list.append(tuple)
            except ValueError:
                continue

        return list

    def get_access_flags(self, channel, nick):
        return self.parent.command("ChanServ", "FLAGS", channel, nick)

    def set_access_flags(self, channel, nick, flags):
        self.parent.command("ChanServ", "FLAGS", channel, nick, "=" + flags)

    def get_channel_info(self, channel):
        data = self.parent.command("ChanServ", "INFO", channel)
        raw_lines = data.split("\n")

        tuple = {}
        for line in raw_lines:
            if line[0] == "*" or "Information on" in line:
                continue

            fields = line.split(" : ", 2)
            try:
                tuple[fields[0].strip()] = fields[1].strip()
            except:
                pass
        return tuple

    def get_channel_flags(self, channel):
        data = self.get_channel_info(channel)
        flags = data["Flags"]

        tuple = {}
        for flag in self.flags:
            if flag in flags:
                tuple[flag] = True
            else:
                tuple[flag] = False

        return tuple

    def set_channel_flag(self, channel, flag, value):
        self.parent.command("ChanServ", "SET", channel, flag, value)


class MemoServ(Parent):
    """
    Parse Atheme MemoServ responses.  Since the XML interface provides the same output as the IRC interface, we
    have to do this.  It"s kind of a pain in the ass.
    """
    def list(self):
        list = []

        data = self.parent.command("MemoServ", "LIST")
        raw_lines = data.split("\n")

        for line in raw_lines:
            if line[0] != "-":
                continue

            data = line.split(" ", 5)
            tuple = {"from": data[3], "sent": data[5]}

            list.append(tuple)

        return list

    def read(self, number):
        data = self.parent.command("MemoServ", "READ", number)
        raw_lines = data.split("\n")

        fields = raw_lines[0].split(" ", 6)
        tuple = {"from": fields[5][0:-1], "sent": fields[6], "message": raw_lines[2]}

        return tuple

    def send(self, target, message):
        self.parent.command("MemoServ", "SEND", target, message)

    def send_ops(self, target, message):
        self.parent.command("MemoServ", "SENDOPS", target, message)

    def send_group(self, target, message):
        self.parent.command("MemoServ", "SENDGROUP", target, message)

    def forward(self, target, message_id):
        self.parent.command("MemoServ", "FORWARD", target, message_id)

    def delete(self, message_id):
        self.parent.command("MemoServ", "DELETE", message_id)

    def ignore_add(self, target):
        self.parent.command("MemoServ", "IGNORE", "ADD", target)

    def ignore_delete(self, target):
        self.parent.command("MemoServ", "IGNORE", "DEL", target)

    def ignore_list(self):
        data = self.parent.command("MemoServ", "IGNORE", "LIST")
        raw_lines = data.split("\n")

        list = []
        for line in raw_lines:
            tuple = {}

            try:
                data = line.split(" ")
                tuple["id"] = int(data[0])
                tuple["account"] = data[2]
                list.append(tuple)
            except ValueError:
                continue

        return list

    def ignore_clear(self):
        self.parent.command("MemoServ", "IGNORE", "CLEAR")


class OperServ(Parent):
    def akill_add(self, mask, reason="Requested"):
        return self.parent.command("OperServ", "AKILL", "ADD", mask, reason)

    def akill_list(self):
        akills = self.parent.command("OperServ", "AKILL", "LIST", "FULL").split("\n")[1:-1]
        akillset = {}

        for i in akills:
            ak = i.split(" - ", 3)
            aki = {"num": int(ak[0].split(" ")[0].strip(":")),
                    "mask": ak[0].split(" ")[1],
                    "setter": ak[1].split(" ")[1],
                    "expiry": ak[2],
                    "reason": ak[3][1:-1]}
            akillset[aki["num"]] = aki

        return akillset

    def akill_del(self, num):
        self.parent.command("OperServ", "AKILL", "DEL", num)

    def kill(self, target):
        return self.parent.command("OperServ", "KILL", target)

    def mode(self, modestring):
        return self.parent.command("OperServ", "MODE", modestring)


class HostServ(Parent):
    """
    Methods for HostServ functionality.
    """

    def activate(self, account):
        self.parent.command("HostServ", "ACTIVATE", account)

    def listvhost(self, mask="*"):
        """
        Return a list of all vhosts (with metadata) by mask
        """
        vhosts = self.parent.command("HostServ", "LISTVHOST", mask)

        reply = []

        for vhost in vhosts.split("\n")[:-1]:
            vhost = vhost.split()
            res = {}

            res["nick"] = vhost[1]
            res["vhost"] = vhost[2]

            reply.append(res)

        return reply

    def request(self, vhost):
        """
        Request a vhost
        """

        self.parent.command("HostServ", "REQUEST", vhost)

    def reject(self, account, reason=None):
        """
        Reject a vhost request
        """

        if reason is not None:
            self.parent.command("HostServ", "REJECT", account, reason)
        else:
            self.parent.command("HostServ", "REJECT", account)

    def waiting(self):
        """
        Get a list of all the vhosts that are waiting to be accepted
        """

        waitinglist = self.parent.command("HostServ", "WAITING").split("\n")
        vhosts = []

        for line in waitinglist:
            nick = line.split("Nick:")[1].split(",")[0]
            vhost = line.split(", vhost:")[1].split(" (")[0]
            date = line.split(" (")[1].split(" - ")[1][:-1]

            vhosts.append({"nick": nick, "vhost": vhost, "date": date})

        return vhosts


class ALIS(Parent):
    """
    Methods for the advanced channel lister
    """

    def list(self, mask="*", popcount=10):
        """
        List channels by mask and/or population count
        """

        data = self.parent.command("ALIS", "LIST", mask, "-min", popcount).split("\n")

        data = data[1:-1] # shuck the data

        chans = []
        for segment in data:
            channel = {}

            if segment == "Maximum channel output reached":
                continue

            segment = segment.split()

            channel["name"] = segment[0]
            channel["safename"] = segment[0][1:]
            channel["population"] = segment[1]
            channel["topic"] = " ".join(segment[2:])[1:]

            chans.append(channel)

        return chans


class InfoServ(Parent):
    """
    InfoServ methods.
    """

    def list(self):
        """
        List all InfoServ news
        """

        data = self.parent.command("InfoServ", "LIST")
        data = data.split("\n")
        data = data[:-1]

        posts = []

        for line in data:
            post = {}

            topic = line.split("[")[1].split("]")[0]
            line  = line.split("[")[1].split("]")[1]

            poster = line.split()[1]
            time = line.split()[3]
            date = line.split()[5][:-1]
            contents = " ".join(line.split()[6:])

            post["poster"] = poster
            post["time"] = time
            post["date"] = date
            post["contents"] = contents
            post["topic"] = topic

            posts.append(post)

        return posts


class AthemeXMLConnection(object):
    def __init__(self, url, ipaddr="0.0.0.0"):
        self.proxy = ServerProxy(url)
        self.chanserv = ChanServ(self)
        self.memoserv = MemoServ(self)
        self.nickserv = NickServ(self)
        self.operserv = OperServ(self)
        self.hostserv = HostServ(self)
        self.infoserv = InfoServ(self)
        self.alis = ALIS(self)
        self._privset = None
        self.ipaddr = ipaddr
        self.username = "*"
        self.authcookie = "*"

    def __getattr__(self, name):
        return self.proxy.__getattr__(name)

    def command(self, service, *parv):
        return self.atheme.command(self.authcookie, self.username, self.ipaddr,
                                   service, *parv)

    def login(self, username, password):
        self.username = username
        self.authcookie = self.atheme.login(username, password)

        self.get_privset()

    def logout(self):
        self.atheme.logout(self.authcookie, self.username)

    def get_privset(self):
        if self._privset is not None:
            return self._privset

        self._privset = self.atheme.privset(self.authcookie, self.username).split()
        return self._privset

    def has_privilege(self, priv):
        try:
            if self.get_privset().index(priv):
                return True
            else:
                return False
        except ValueError:
            return False

    def register(self, username, password, email):
        try:
            return self.atheme.command("*", "*", self.ipaddr, "NickServ", "REGISTER", username, password, email)
        except Fault, e:
            if e.faultString == "A user matching this account is already on IRC.":
                return "Error: " + e.faultString + "  If you are already connected to IRC using this nickname, please complete the registration procedure through IRC."

            return "Error: " + e.faultString


class CodAthemeConnector():
    def __init__(self, cod):
        self.cod = cod
        self.xmlrpc = cod.config["atheme"]["xmlrpc"]
        if self.xmlrpc and len(self.xmlrpc):
            self.atheme = AthemeXMLConnection(self.xmlrpc)
            self.__login()

    def __login(self):
        self.atheme.login(self.cod.config["me"]["nick"],
                          self.cod.config["me"]["servicespass"])
        self.time = time.time()

        self.cod.log("Logged into XMLRPC")

    def __getattr__(self, name):
        if self.time + 600 < time.time():
            self.__login()

        if hasattr(self.atheme, name):
            return getattr(self.atheme, name)
        else:
            return object().__getattr__(self, name)
