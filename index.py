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
	
		values = {
		}
		self.response.out.write(template.render('templates/index.html', values))    
		            
    def post(self):
		subscriber = Subscriber(
			who = self.request.get('email'))
		subscriber.put()
		self.response.out.write('Great Success!');
		
def main():
    app = webapp.WSGIApplication([
        (r'.*', MainHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()