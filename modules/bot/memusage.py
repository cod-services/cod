import os
import re

"""
Code from skybot
"""

NAME="memusage"
DESC="Shows memory usage statistics"

def initModule(cod):
    cod.addBotCommand("MEM", cmdMEM, True)

def destroyModule(cod):
    cod.delBotCommand("MEM")

def rehash():
    pass

def cmdMEM(cod, line, splitline, source, destination):
    cod.reply(source, destination, mem() + " %d clients, %d channels" %\
            (len(cod.clients), len(cod.channels)))

def mem():
    status_file = open("/proc/%d/status" % os.getpid()).read()
    line_pairs = re.findall(r"^(\w+):\s*(.*)\s*$", status_file, re.M)
    status = dict(line_pairs)
    keys = 'VmSize VmLib VmData VmExe VmRSS VmStk'.split()

    return ', '.join(key + ':' + status[key] for key in keys)

