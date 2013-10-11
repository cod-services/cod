import json
import sys

class Config():
    """
    This is a very basic configuration file parser class.

    You can access the config loaded with the element name
    "config" in an instance of this class.
    """
    def __init__(self, cfilepath):
        """
        Inputs: config file path

        Loads the configuration file specified into memory.
        """
        self.cfilepath = cfilepath

        try:
            with open(cfilepath, "r") as cfile:
                configstr = cfile.read()

                self.config = json.loads(configstr)
        except IOError as e:
            print "Config file not found or readable %s" % cfilepath
            sys.exit(-1)

