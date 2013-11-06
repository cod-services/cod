from utils import *
from structures import *
from random import choice
from random import randint

NAME="Operation Name Generator"
DESC="Generates something that could pass as a military operation name in a B-movie"

prefix = []
suffix = []

def initModule(cod):
    global prefix, suffix

    prefix = []

    suffix = []

    #Read prefix and suffix lines in
    with open(cod.config["etc"]["prefixfile"], 'r') as prefixfile:
        cod.log("Reading in prefixes from %s" % cod.config["etc"]["prefixfile"], "===")
        prefix = prefixfile.readlines()
    with open(cod.config["etc"]["suffixfile"], 'r') as suffixfile:
        cod.log("Reading in suffixes from %s" % cod.config["etc"]["suffixfile"], "===")
        suffix = suffixfile.readlines()

    #Strip lines and prune junk lines
    for ix in [prefix, suffix]:
        for junk in range(len(ix)-1, -1, -1):
            ix[junk] = ix[junk].strip()

    #Register bot command
    cod.botcommands["OPNAME"] = [commandOPNAME]

def destroyModule(cod):
    global prefix, suffix

    del prefix
    del suffix

    del cod.botcommands["OPNAME"]

def rehash():
    pass

def commandOPNAME(cod, line, splitline, source, destination):
    global prefix, suffix

    #Create phrase
    phrase = "OPERATION %s %s %s" % \
                (choice(prefix), choice(prefix), choice(suffix))

    cod.reply(source, destination, phrase.upper())

