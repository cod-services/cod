"""
Copyright (c) 2013, Sam Dodrill
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

NAME="Relay HostServ"
DESC="Relays HostServ lines in snoop channel to staff channel"

TLDLIST = []

def initModule(cod):
    global TLDLIST

    cod.s2scommands["PRIVMSG"].append(relayHostServToOpers)

    with open("var/tlds-alpha-by-domain.txt", "r") as tlds:
        for line in tlds.readlines():
            TLDLIST.append(line.strip())

def destroyModule(cod):
    cod.s2scommands["PRIVMSG"].remove(relayHostServToOpers)

def rehash():
    pass

def anyOf(things, check):
    for thing in things:
        if thing in check:
            return True

    return False

def relayHostServToOpers(cod, line):
    global TLDLIST

    if line.args[0] == cod.config["etc"]["snoopchan"]:
        if cod.clients[line.source].nick == "HostServ":
            if anyOf(["TAKE", "REQUEST", "REJECT", "ASSIGN", "LISTVHOST"], line.args[-1]):
                cod.sendLine(cod.client.privmsg(cod.config["etc"]["staffchan"],
                    "HostServ: " + line.args[-1]))

            splitline = line.args[-1].split()

            if len(splitline) < 3:
                return

            vhost = ""
            place = 0

            if splitline[1] == "REQUEST:":
                vhost = splitline[2][1:-1] #shuck the vhost
            elif splitline[2] == "REQUEST:":
                vhost = splitline[3][1:-1] #shuck the vhost
                place = 1
            else:
                return

            splithost = vhost.split(".")

            print splithost[-1].upper()

            for tld in TLDLIST:
                if splithost[-1].upper() == tld:
                    requester = splitline[0]

                    cod.privmsg(cod.findClientByNick("HostServ").uid,
                               "REJECT %s Your chosen VHost (%s) is a real domain name and cannot be chosen as a VHost. Please contact an operator in %s." %\
                               (requester, vhost, cod.config["etc"]["helpchan"]))
                    return

            for frag in splithost:
                #don't look up "to", "a", etc
                if len(frag) < 3:
                    continue

                if len(frag) < 7:
                    frag = "*%s*" % frag
                else:
                    frag = "*%s*" % frag[2:-2]

                cod.privmsg(cod.findClientByNick("HostServ").uid,
                            "LISTVHOST %s" % frag)

