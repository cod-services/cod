from client import *

def handleEUID(cod, line, splitline, source):
    client = Client(splitline[2], splitline[9], splitline[4], splitline[5], splitline[6], splitline[7], splitline[8], splitline[11], splitline[12][1:])

    cod.clients[client.uid] = client

def handleQUIT(cod, line, splitline, source):
    cod.clients.pop(source)

def handleSJOIN(cod, line, splitline, source):
    try:
        cod.channels[splitline[3]]
    except KeyError as e:
        cod.channels[splitline[3]] = Channel(splitline[3], splitline[2])
    finally:
        uids = line.split(":")[2].split(" ")
        for uid in uids:
            #Extremely pro implementation

            prefix = uid[:-9]

            uid = uid[-9:]

            client = cod.clients[uid]

            #I warned you this was shitty
            cod.channels[splitline[3]].clientAdd(client, prefix)

def handleNICK(cod, line, splitline, source):
    cod.clients[source].nick = splitline[2]

def handleBMASK(cod, line, splitline, source):
    list = splitline[4]

    #The channel will be a valid channel
    channel = cod.channels[splitline[3]]

    channel.lists[list].append([n for n in line.split(":")[2].split(" ")])

def handleMODE(cod, line, splitline, source):
    extparam = line.split(":")[2]

    if extparam.find("o") != -1:
        if extparam[0] == "+":
            cod.clients[source].isOper = True
        else:
            cod.clients[sourcd].isOper = False

