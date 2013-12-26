"""
Copyright (c) 2013, Sam Dodrill, Jessica Williams
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

import threading
import time
from pyrrd.rrd import DataSource, RRA, RRD

timer = None
myRRD = None

def initModule(cod):
    global myRRD

    dataSources = []
    roundRobinArchives = []

    dataSource = DataSource(
            dsName="clients", dsType="GAGUE", heartbeat=300)

    dataSources.append(dataSource)

    roundRobinArchives.append(RRA(cf='AVERAGE', xff=0.5, steps=1, rows=24))
    roundRobinArchives.append(RRA(cf='AVERAGE', xff=0.5, steps=6, rows=10))

    myRRD = RRD(
            cod.config["rrd"]["clients"], ds=dataSources, rra=roundRobinArchives)

    makeTimer(cod, countUsers, 300)

def destroyModule(cod):
    global timer

    timer.cancel()
    del timer

def makeTimer(cod, func, interval):
    global timer

    timer = threading.Timer(interval, func, args=[cod, func, interval])
    timer.start()

def delTimer():
    global timer

    timer.cancel()
    del timer

def refresh(cod, func, interval):
    delTimer()
    makeTimer(cod, func, interval)

def countUsers(cod, func, interval):
    global myRRD

    cod.log("CLIENTS: %d" % len(cod.clients))

    myRRD.bufferValue(`int(time.time())`, len(cod.clients))
    myRRD.update()

    refresh(cod, func, interval)

