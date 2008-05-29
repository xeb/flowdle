#!/usr/bin/env python

import wsgiref.handlers
import models
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):
    def get(self):
		user = users.get_current_user()
		values = {
			'user': user,
			'signout' : users.create_logout_url("/"),
			'taglist' : 'None'
		}
		self.response.out.write(template.render('templates/app.html', values))    
		
def main():
    app = webapp.WSGIApplication([
        (r'.*', MainHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()