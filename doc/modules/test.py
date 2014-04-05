"""
Copyright (c) 2014, Sam Dodrill
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

from structures import *
from utils import *

"""
Example test module
"""

#All modules have a name and description
NAME="Test module"
DESC="Small example to help you get started"

def initModule(cod):
    """
    This function is called when the module is initialized. All bot or s2s
    commands must be declared here for them to be recognized.
    """
    cod.addBotCommand("TEST", testbotCommand)
    cod.s2scommands["TEST"] = [tests2sCommand]

def destroyModule(cod):
    """
    This function is called when the module is being destroyed. All bot, s2s
    commands and any side effects must be deleted here.
    """
    cod.delBotCommand("TEST")
    del cod.s2scommands["TEST"]

def rehash():
    """
    This function is called when a rehash is being done. If you need anything
    to be done on a rehash, do it here.
    """

    pass

def testbotCommand(cod, line, splitline, source, destination):
    "A simple test command"

    """
    A bot command takes in 5 arguments:

    1. A reference to the cod instance
    2. The line cut after the server command
    3. The line split by spaces for convenience
    4. The source UID of the message
    5. The destination of the message, can be UID or channel

    A bot command may either return a reply or send one directly. It is preferable
    to return a reply directly to make it work with JSON-RPC.
    """

    return "Hello!"

def tests2sCommand(cod, line):
    """
    A s2s command takes in 2 arguments:

    1. A reference to the cod instance
    2. An IRCLine instance with the line from the server pre-populated
    """

    pass

