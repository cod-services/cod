from random import choice, random, randint
import time

COLORS = ['03','04','06','07','08','09','10','11','12','13']

#Shibe generation code borrowed from aji

class pvec:
    def __init__(self, num):
        self.v = [1.0] * num
        self.norm()
    def norm(self):
        s = sum(self.v)
        self.v = [x / s for x in self.v]
    def pick(self):
        r = random() * sum(self.v) # sum should always be 1, but meh
        s = 0
        for i, x in enumerate(self.v):
            s += x
            if r < s:
                break
        def calc(j, x):
            fac = (1 - 3.5 / (abs(i - j) + 4.5))
            return x * fac
        self.v = [calc(j, x) for j, x in enumerate(self.v)]
        self.norm()
        return i

spvec = pvec(40)
for i in range(10):
    spvec.pick()

last_color = '00'

def gen_prefix():
    global last_color

    color = choice(COLORS)
    while color == last_color:
        color = choice(COLORS)

    last_color = color
    return ' ' * spvec.pick() + '\3' + color

NAME="Shibe"
DESC="Wow, such bot command"

def initModule(cod):
    cod.addBotCommand("SHIBE", wowSuchImplementation)

def destroyModule(cod):
    cod.delBotCommand("SHIBE")

def wowSuchImplementation(cod, line, splitline, source, destination):
    cod.reply(source, destination, "%s%s" %\
            (gen_prefix(), " ".join(splitline[1:])))

