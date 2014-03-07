"""
Simple relay from #help tp #opers

Code is in public domain
"""

DESC="Relay messages from the help channel to the staff channel"

def initModule(cod):
    cod.addHook("chanmsg", chanmsgHook)

def destroyModule(cod):
    cod.delHook("chanmsg", chanmsgHook)

def chanmsgHook(cod, target, line):
    if target.name == cod.config["etc"]["helpchan"]:
        cod.privmsg(cod.config["etc"]["staffchan"], "%s: <-%s> %s" %\
                (target.name, line.source.nick, line.args[-1]))

