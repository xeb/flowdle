#!/usr/bin/env python

import wsgiref.handlers
#from current import flowdlemodels

from models import BetaRequest
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('../templates/index.html', None))    
        #self.redirect('/closed')


class ClosedHandler(webapp.RequestHandler):
    def get(self):
        if users.is_current_user_admin():
            self.redirect('/app')
        else:
            self.response.out.write(template.render('../templates/index.html', None))
    
    def post(self):
        req = BetaRequest(who=self.request.get('who'))
        req.put()
        #self.redirect('/closed/thankyou')
        
        
class ThankYouHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('../templates/thankyou.html', None))
        

def main():
    app = webapp.WSGIApplication([
        ('/', ClosedHandler),
        ('/index.html', ClosedHandler),
        ('/closed', ClosedHandler),
        ('/closed/', ClosedHandler),
        ('/closed/thankyou', ThankYouHandler)], debug=False)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()