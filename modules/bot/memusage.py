import os
import re

NAME="memusage"
DESC="Shows memory usage statistics"

def initModule(cod):
    cod.botcommands["MEM"] = [cmdMEM]

def destroyModule(cod):
    del cod.botcommands["MEM"]

def rehash():
    pass

def cmdMEM(cod, line, splitline, source, destination):
    cod.reply(source, destination, mem())

def mem():
    status_file = open("/proc/%d/status" % os.getpid()).read()
    line_pairs = re.findall(r"^(\w+):\s*(.*)\s*$", status_file, re.M)
    status = dict(line_pairs)
    keys = 'VmSize VmLib VmData VmExe VmRSS VmStk'.split()

    return ', '.join(key + ':' + status[key] for key in keys)

