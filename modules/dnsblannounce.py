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
    idx = cod.s2scommands["ENCAP"].index(announceDNSBLHits)
    cod.s2scommands.pop(idx)

def announceDNSBLHits(cod, line, splitline, source):
    if splitline[3] == "SNOTE":
        if splitline[4] == "r":
            message = line.split(":")[2]
            cod.servicesLog("DNSBL:HIT: %s" % message)

            try:
                ip = message.split()[1].split("@")[1][:-1]
            except:
                return

            cod.servicesLog("Checking %s in %d blacklists..." %(ip, len(rblwatch.RBLS)))

            search = rblwatch.RBLSearch(cod, ip)
            search.print_results()

