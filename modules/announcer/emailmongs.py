"""
Copyright (c) 2014, Sam Dodrill
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

import codemail
import socket
import time

from mako.template import Template
from querycontacts import ContactFinder

NAME="Mong emailer"
DESC="Sends abuse complaints to the providers of idiots that POST an ircd"

template = """Hello,

This is an automated message. An IP address you control (${ip})
has made a POST request to port 5000 of the ircd at ${server}. This could mean
the machine at that IP address is compromised or is doing scanning for a certain
kind of vulnerable system. If at all possible, please discontinue
${ip}'s attempts to POST this network's daemons.

As this is an automated message, replies will be ignored. If you wish to email
the network staff directly, please do so to ${replymail}. Another option is to
connect with any standard irc client to ${server} and join ${helpchan}.

This email was sent at ${time} and the protocol line that triggered it was:

    ${line}

A full record of all information that our IRC daemon reported:

    hostname of client: ${host} (${ip})
    server affected: ${server}

Thank you for your understanding. This message is in your inbox because
${email} is listed as your email in a WHOIS lookup.
If this is in error, please send a full copy of this message to ${replymail}
with a timestamp in GMT so a false positive can be recorded as well as steps
taken to prevent future emails like this one from being sent.

${network} Staff
"""

def initModule(cod):
    cod.s2scommands["ENCAP"].append(emailMongs)

def destroyModule(cod):
    cod.s2scommands["ENCAP"].remove(emailMongs)

def rehash():
    pass

def emailMongs(cod, line):
    if line.args[1] == "SNOTE":
        if line.args[2] == "r":
            message = line.args[-1]

            if "HTTP Proxy" not in message:
                return

            email = codemail.Email(cod)
            qf = ContactFinder()

            host = message.split("@")[1][:-1]
            ip = socket.gethostbyname(host)
            server = message.split()[0]
            now = time.ctime()
            network = cod.config["me"]["netname"]
            helpchan = cod.config["etc"]["helpchan"]

            replymail = "staff@%s" % email.config.myemail.split("@")[1]

            if host == ip:
                subject = "HTTP Proxy connection attempt from %s" % (ip)
            else:
                subject = "HTTP Proxy connection attempt from %s (%s)" % (host, ip)

            cod.servicesLog(subject + " on server %s" % server)

            my_template = Template(template)

            emails = qf.find(ip)

            for address in emails:
                text = my_template.render(ip=ip, server=server, replymail=replymail,
                        time=now, line=str(line), helpchan=helpchan, email=address,
                        network=network, host=host)

                email.format_email(address, subject, text)

