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

import requests

NAME="eval.appspot.org eval"
DESC="sandboxed Python evaluator"

def initModule(cod):
    cod.addBotCommand("EVAL", eval_line)

def destroyModule(cod):
    cod.delBotCommand("EVAL")

def rehash():
    pass

def eval_line(cod, line, splitline, source, destination):
    "Uses a Google sandbox to evaluate python code"

    try:
        code = " ".join(splitline[1:])

        if code == "":
            cod.reply(source, destination, "Need code to eval")
            return

        reply = requests.get("http://eval.appspot.com/eval?statement=%s" % code)

        output = reply.text

        if "\r" in output:
            output = output.split("\r")[0]

        if "\n" in output:
            output = output.split("\n")[0]

        if len(output) > 400:
            output = output[:399]

        cod.reply(source, destination, "> %s" % str(output))

    except Exception as e:
        cod.reply(source, destination, "There was some error: %s" % e.message)

