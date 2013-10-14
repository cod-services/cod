"""
Copyright (c) 2013, Sam Dodrill
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

  Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

            ip = message.split()[1].split("@")[1][:-1]

            cod.servicesLog("Checking %s in %d blacklists..." %(ip, len(rblwatch.RBLS)))

            search = rblwatch.RBLSearch(cod, ip)
            search.print_results()

