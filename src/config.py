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

