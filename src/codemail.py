"""
Copyright (c) 2014 Sam Dodrill
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

import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# Trying this here.
# http://stackoverflow.com/a/14620633/753355
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class Email(object):
    def __init__(self, cod):
        self.cod = cod

        self.config = AttrDict(self.cod.config["email"])

    def send_email(self, target, message):
        server = smtplib.SMTP(self.config.host, self.config.port)
        server.login(self.config.username, self.config.password)

        server.sendmail(self.config.myemail, target, message)

        self.cod.servicesLog("Email sent to %s." % (target))

    def format_email(self, target, subject, message):
        msg = MIMEMultipart()
        msg['From'] = self.config.myemail
        msg['To'] = target
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        text = msg.as_string()

        self.send_email(target, text)

