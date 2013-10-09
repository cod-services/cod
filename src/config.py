import json
import sys

class Config():
    def __init__(self, cfilepath):
        self.cfilepath = cfilepath

        try:
            with open(cfilepath, "r") as cfile:
                configstr = cfile.read()

                self.config = json.loads(configstr)
        except IOError as e:
            print "Config file not found or readable %s" % cfilepath
            sys.exit(-1)

