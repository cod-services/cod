from client import *

def handleEUID(cod, line, splitline, source):
    print "New client %s on the network" % splitline[2]
    cod.clients[splitline[9]] = Client(splitline[2], splitline[9], splitline[4], splitline[5], splitline[6], splitline[7], splitline[8], splitline[11], splitline[12][1:])

def handleQUIT(cod, line, splitline, source):
    print "Quit: %s" % clients[source].nick
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

            #print "%s: %s%s" % (splitline[3], prefix, client.nick)

