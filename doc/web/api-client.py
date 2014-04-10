"""
This file is under the Cod license
"""

import requests


class CodConnector:
    def __init__(self, rpcpath):
        self.rpcpath = rpcpath

    def command(self, command, args=[]):
        req = requests.get("%s/json/command?cmd=%s" %
                           (self.rpcpath, command.upper())).json()

        return req["output"] if req["status"] == "okay" else []

    def channel_info(self, channel=None):
        # If channel = None, get all info about all channels

        if channel is None:
            req = requests.get("%s/json/chaninfo" % self.rpcpath).json()

            return req["output"] if req["status"] == "okay" else []

    def client_info(self):
        req = requests.get("%s/json/clientinfo" % self.rpcpath).json()

        return req["output"] if req["status"] == "okay" else []
