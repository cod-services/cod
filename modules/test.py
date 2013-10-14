"""
Copyright (c) 2013, Sam Dodrill
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

  Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

