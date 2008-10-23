#!/usr/bin/env python

import wsgiref.handlers
#from current import flowdlemodels

from models import BetaRequest
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class SettingsHandler(webapp.RequestHandler):
    def get(self):
        
        user = users.get_current_user()
        
        values = {
            'user' : user
        }
        self.response.out.write(template.render('../templates/settings.html', values))    
        #self.redirect('/closed')


def main():
    app = webapp.WSGIApplication([
        ('/settings', SettingsHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()