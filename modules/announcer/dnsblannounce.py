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

import rblwatch

NAME="dnsbl announce"
DESC="Announces DNSBL hits and does lookups on them"

def initModule(cod):
    cod.s2scommands["ENCAP"].append(announceDNSBLHits)

def destroyModule(cod):
    cod.s2scommands["ENCAP"].remove(announceDNSBLHits)

def rehash():
    pass

def announceDNSBLHits(cod, line):
    if line.args[1] == "SNOTE":
        if line.args[2] == "r":
            message = line.args[-1]

            if "DNS" not in message:
                return

            cod.servicesLog("DNSBL:HIT: %s" % message)

            try:
                ip = message.split()[1].split("@")[1][:-1]
            except:
                return

            cod.servicesLog("Checking %s in %d blacklists..." %(ip, len(rblwatch.RBLS)))

            search = rblwatch.RBLSearch(cod, ip)
            search.print_results()

