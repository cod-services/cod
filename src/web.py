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

import cherrypy
from mako.lookup import TemplateLookup


class RootPage:
    def __init__(self, cod):
        self.cod = cod

        self.pages = []

    def add_page(self, name, Page):
        setattr(self, name, Page(self.cod))
        self.pages.append(name)

    def del_page(self, name):
        delattr(self, name)
        self.pages.remove(name)

    @cherrypy.expose
    def index(self):
        return "Hello!"

# http://tools.cherrypy.org/wiki/Mako

class MakoHandler(cherrypy.dispatch.LateParamPageHandler):
    """Callable which sets response.body."""

    def __init__(self, template, next_handler):
        self.template = template
        self.next_handler = next_handler

    def __call__(self):
        env = globals().copy()
        env.update(self.next_handler())
        try:
            return self.template.render(**env)
        except:
            # something went wrong rendering the template
            # this will generate a pretty error page with details
            cherrypy.response.status = "500"
            return exceptions.html_error_template().render()

class MakoLoader(object):

    def __init__(self):
        self.lookups = {}

    def __call__(self, filename, directories, module_directory=None,
                 collection_size=-1):
        # Find the appropriate template lookup.
        key = (tuple(directories), module_directory)
        try:
            lookup = self.lookups[key]
        except KeyError:
            lookup = TemplateLookup(directories=directories,
                                    module_directory=module_directory,
                                    collection_size=collection_size,
                                    )
            self.lookups[key] = lookup
        cherrypy.request.lookup = lookup

        # Replace the current handler.
        cherrypy.request.template = t = lookup.get_template(filename)
        cherrypy.request.handler = MakoHandler(t, cherrypy.request.handler)

main = MakoLoader()
cherrypy.tools.mako = cherrypy.Tool('on_start_resource', main)

