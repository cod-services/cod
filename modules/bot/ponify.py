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

import re
import json

list_of_finds = []

NAME="Ponify"
DESC="Ponyfy words or phrases"

def initModule(cod):
    global list_of_finds

    cod.botcommands["PONIFY"] = [ponifyCMD]
    list_of_finds = json.load(open("etc/ponifylist.json"))
    list_of_finds = list(map(lambda x: [bytes(s) for s in x[:2]], list_of_finds))

def destroyModule(cod):
    del cod.botcommands["PONIFY"]

def rehash():
    pass

def ponifyCMD(cod, line, splitline, source, destination):
    global list_of_finds

    line = " ".join(splitline[1:])

    cod.reply(source, destination, "%s: %s" %
            (cod.clients[source].nick, replace(line, list_of_finds)))

def map_each(replacements, f):
    return list(list(map(f, entry)) for entry in replacements)

# add titles and ALL CAPS
list_of_finds += map_each(list_of_finds, str.title) + map_each(list_of_finds, str.upper)


def replace(text, replacements=list_of_finds):
	for number in range(len(replacements)):
		find = replacements[number][0]
		text = text.replace(find, replacements[number][1])

	return str(text)


def undo_replace(text, replacements=list_of_finds):
        for number in range(len(replacements)):
                find = replacements[number][1]
                text = text.replace(find, replacements[number][0])

        return text

