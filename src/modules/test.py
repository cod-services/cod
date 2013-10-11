from structures import *
from utils import *

def initModule(cod):
    cod.botcommands["TEST"] = [commandTEST]

def destroyModule(cod):
    del cod.botcommands["TEST"]

def commandTEST(cod, line, splitline, source, destination):
    reply(cod, source, destination, "Hello!")

