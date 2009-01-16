#!/usr/bin/env python

import wsgiref.handlers
#from current import flowdlemodels

from models import BetaRequest
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import mail
from google.appengine.ext.webapp import template


class FeedbackHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('../templates/feedback.html', None))    
            
    def post(self):
        user = users.get_current_user()
        message = mail.EmailMessage(sender="no-reply@flowdle.com",
                  to="mark@kockerbeck.com",
                  subject="Flowdle Feedback: " + self.request.get('subject')[:50],
                  body= self.request.get('message') + "\n\n http://www.flowdle.com/")        
        message.send()
        self.response.out.write(template.render('../templates/thankyou.html', None))
        
def main():
    app = webapp.WSGIApplication([
        ('/feedback', FeedbackHandler)], debug=False)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()