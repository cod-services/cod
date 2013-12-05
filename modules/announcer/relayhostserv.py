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

def initModule(cod):
    cod.s2scommands["PRIVMSG"].append(relayHostServToOpers)

def destroyModule(cod):
    cod.s2scommands["PRIVMSG"].remove(relayHostServToOpers)

def rehash():
    pass

def relayHostServToOpers(cod, line):
    if line.args[0] == cod.config["etc"]["snoopchan"]:
        if cod.clients[line.source].nick == "HostServ":
            cod.sendLine(cod.client.privmsg(cod.config["etc"]["staffchan"],
                "HostServ: " + line.args[-1]))

            splitline = line.args[-1].split()

            vhost = ""

            if splitline[1] == "REQUEST:":
                vhost = splitline[2][1:-1] #shuck the vhost
            elif splitline[2] == "REQUEST:":
                vhost = splitline[3][1:-1] #shuck the vhost
            else:
                return

            print vhost.split(".")

            for frag in vhost.split("."):
                if len(frag) < 5:
                    frag = "*%s*" % frag
                else:
                    frag = "*%s*" % frag[2:-2]

                print frag

                cod.privmsg(cod.findClientByNick("HostServ").uid,
                            "LISTVHOST %s" % frag)

