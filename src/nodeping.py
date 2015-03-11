"""
Copyright (c) 2013-2014, Christine Dodrill
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

import requests

class JsonException(Exception):
    pass

class NodePing:
    def __init__(self, apikey):
        self.key = apikey

    def request(self, path):
        url = "https://api.nodeping.com/api/1/%s?token=%s" % (path, self.key)
        json = requests.get(url).json()
        if "error" in json:
            raise JsonException
        else:
            return json

    def get_checks(self, by=None):
        checks = self.request("checks")

        if by != None:
            mychecks = filter((lambda x: by in checks[x]["label"]), checks)

            return [checks[x] for x in checks if x in mychecks]
        else:
            return checks

    def get_uptime(self, check):
        if "uuid" in check:
            check = check["uuid"]

        reply = requests.get("https://nodeping.com/reports/uptime/%s?format=json&token=%s" %
                (check, self.key)).json()

        if "error" in reply:
            raise JsonException
        else:
            return reply

