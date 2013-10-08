import json

class Config():
    def __init__(self, cfilepath):
        self.cfilepath = cfilepath

        with open(cfilepath, "r") as cfile:
            configstr = cfile.read()

            self.config = json.loads(configstr)
