"""
Test code by Donut Steel

This creates a webpage at /test
"""

import cherrypy

from web import RootPage

def initModule(cod):
    cod.webapp.root.add_page("test", TestPage)

def destroyModule(cod):
    cod.webapp.root.del_page("test")

class TestPage(RootPage):
    def __init__(self, cod):
        self.cod = cod

    @cherrypy.expose
    def index(self):
       return "Cod version %s" % self.cod.version

