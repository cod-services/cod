"""
Test code by Donut Steel

Don't steal.
"""

def initModule(cod):
    """
    Hooks are added with cod.addHook(<hookname>, <hookfunc>).
    """

    cod.addHook("test", testFunc)
    cod.addHook("privmsg", privmsgHook)
    cod.addHook("chanmsg", chanmsgHook)
    cod.addHook("newclient", newClientHook)
    cod.addHook("join", joinHook)

    """
    Hooks are executed by cod.runHooks(<hookname>, [<hookargs>]).
    IT IS VITAL THAT THE HOOK ARGUMENTS BE A LIST.
    """

    cod.runHooks("test", ["Hi from a hook!"])

def destroyModule(cod):
    """
    For now, all hooks must be deleted from the table manually.
    """

    cod.delHook("test", testFunc)
    cod.delHook("privmsg", privmsgHook)
    cod.delHook("chanmsg", chanmsgHook)
    cod.delHook("join", joinHook)
    cod.delHook("newclient", newClientHook)

# A join hook expects the arguments to be the source client instance and the
# destination channel instance.
def joinHook(cod, client, channel):
    cod.log("%s joined to %s" % (client.nick, channel.name))

# A newclient hook expects that the argument will be a client instance of the
# client that just connected to the network.
def newClientHook(cod, client):
    cod.log("New client %s" % client.nick)

# A chanmsg hook expects the name of the channel and the IRCMessage line as
# arguments. It is called when a channel message is recieved.
def chanmsgHook(cod, target, line):
    cod.log("%s <%s> %s" % (target, line.source.nick, line.args[-1]))

# A privmsg hook sends the client object for the target and the sender as
# arguments. It is called when a client private messages a services bot
def privmsgHook(cod, target, line):
    cod.log("%s <%s> %s" % (target.nick, line.source.nick, line.args[-1]))

# A demonstration on how to add your own hooks
def testFunc(cod, string):
    cod.servicesLog(string)

