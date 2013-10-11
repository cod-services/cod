from structures import *
from utils import *

"""
Example test module
"""

def initModule(cod):
    """
    This function is called when the module is initialized. All bot or s2s
    commands must be declared here for them to be recognized.
    """
    cod.botcommands["TEST"] = [testbotCommand]
    cod.s2scommands["TEST"] = [tests2sCommand]

def destroyModule(cod):
    """
    This function is called when the module is being destroyed. All bot, s2s
    commands and any side effects must be deleted here.
    """
    del cod.botcommands["TEST"]
    del cod.s2scommands["TEST"]

def testbotCommand(cod, line, splitline, source, destination):
    """
    A bot command takes in 5 arguments:

    1. A reference to the cod instance
    2. The line cut after the server command
    3. The line split by spaces for convenience
    4. The source UID of the message
    5. The destination of the message, can be UID or channel
    """
    cod.reply(source, destination, "Hello!")

def tests2sCommand(cod, line, splitline, source):
    """
    A s2s command takes in 4 arguments:

    1. A reference to the cod instance
    2. The line from the server
    3. The line split by spaces for convenience
    4. The source user or server ID of the message
    """
    pass

