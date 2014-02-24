"""
Copyright (c) 2013-2014, Sam Dodrill
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

class IRCLine:
    def __init__(self, line, p10=False):
        self.line = line

        splitline = line.split()

        self.p10 = p10

        args = []

        if p10:
            self.source = splitline[0]
            self.verb = splitline[1]
            args = splitline[2:]
        else:
            if line.startswith(":"):
                self.source = splitline[0][1:]
                self.verb = splitline[1]
                args = splitline[2:]
            else:
                self.source = None
                self.verb = splitline[0]
                args = splitline[1:]

        for arg in args:
            if arg.startswith(":"):
                index = args.index(arg)
                arg = " ".join(args[index:])
                arg = arg[1:]
                args = args[:index]

                args.append(arg)

                break
        self.args = args

    def __str__(self):
       return self.line
