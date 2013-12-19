"""
Copyright (c) 2013, Sam Dodrill
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

NAME="Weather lookups"
DESC="Reads information from http://worldweatheronline.com"

import requests
from bs4 import BeautifulSoup

apikey = ""

def initModule(cod):
    global apikey

    apikey = cod.config["apikeys"]["worldweatheronline"]

    cod.botcommands["WEATHER"] = [commandWEATHER]

def destroyModule(cod):
    del cod.botcommands["WEATHER"]

def commandWEATHER(cod, line, splitline, source, destination):
    global apikey

    location = " ".join(splitline[1:])

    try:
        #XXX: There has got to be a better way to do this.
        html = requests.get("http://thefuckingweather.com/?where=%s&unit=c" % location)
        soup = BeautifulSoup(html.text)
        locale = soup('span', {"id": "locationDisplaySpan"})[0].getText()

        weatherInfo = requests.get("http://api.worldweatheronline.com/free/v1/weather.ashx?key=%s&num_of_days=1&format=json&q=%s" % (apikey, location)).json()

        temps = (weatherInfo["data"]["current_condition"][0]["temp_F"],
                weatherInfo["data"]["current_condition"][0]["temp_C"])

        wind = "With wind blowing from the %s at %s km/h" %\
                (weatherInfo["data"]["current_condition"][0]["winddir16Point"],
                        weatherInfo["data"]["current_condition"][0]["windspeedKmph"])

        if locale == "":
            locale = location

        cod.reply(source, destination, "Weather report for %s: %s degrees C (%s F), %s" %\
                (locale, temps[1], temps[0], wind))

    except:
        cod.reply(source, destination, "%s: %s doesn't seem to be a valid location" %\
                (cod.clients[source].nick, location))

