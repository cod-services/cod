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

from utils import *
from structures import *

NAME="dnsbl"
DESC="Does DNSBL lookups by nick or IP address"

import rblwatch

def initModule(cod):
    cod.botcommands["RBL"] = [commandRBL]

def destroyModule(cod):
    del cod.botcommands["RBL"]

def commandRBL(cod, line, splitline, source, destination):
    if failIfNotOper(cod, cod.clients, cod.clients[source]):
        return

    search = None
    target = splitline[1]

    if splitline[1].find(".") == -1:
        #If we don't have an IP address, we have a nick of a client
        mark = None

        client = cod.findClientByNick(target)

        if client == None:
            cod.notice(source, "Error: %s is not on IRC" % mark)
            return

        if client.ip == "0":
            cod.notice(source, "Error: target %s is a network service" % client.nick)
            return

        target = client.ip

    cod.servicesLog("RBL: %s: %s" % (target, cod.clients[source].nick))

    search = rblwatch.RBLSearch(cod, target)

    search.print_results()

