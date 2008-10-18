#!/usr/bin/env python

import wsgiref.handlers
import models
from models import Subscriber
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):
    def get(self):
        #self.response.out.write(template.render('../templates/index.html', None))    
        self.redirect('/closed')


class ClosedHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('../templates/closed.html', None))
    
    def post(self):
        sub = Subscriber(who=self.request.get('who'))
        sub.put()
        self.redirect('/closed/thankyou')
        
        
class ThankYouHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('../templates/thankyou.html', None))
        

def main():
    app = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/index.html', MainHandler),
        ('/closed', ClosedHandler),
        ('/closed/', ClosedHandler),
        ('/closed/thankyou', ThankYouHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()