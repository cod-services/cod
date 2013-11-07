import re
import json

list_of_finds = []

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

