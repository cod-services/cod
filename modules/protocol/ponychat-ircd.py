NAME="ponychat-ircd protocol module"
DESC="Handles login for ponychat-ircd"

def initModule(cod):
    cod.loginFunc = login

def destroyModule(cod):
    del cod.loginFunc
    cod.loginFunc = None

def login(cod):
    cod.sendLine("PASS %s TS 6 :%s" % \
            (cod.config["uplink"]["pass"], cod.config["uplink"]["sid"]))
    cod.sendLine("CAPAB :QS EX IE KLN UNKLN ENCAP SERVICES EUID EOPMOD")
    cod.sendLine("SERVER %s 1 :%s" % \
            (cod.config["me"]["name"], cod.config["me"]["desc"]))

