#!/usr/bin/env python

import wsgiref.handlers
#from current import flowdlemodels

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            self.redirect(users.create_logout_url("/"))
        else:
            self.redirect('/')
            
def main():
    app = webapp.WSGIApplication(
                [('/logout', MainHandler)], 
                debug=False)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()