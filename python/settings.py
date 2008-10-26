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
        sub = db.GqlQuery('SELECT * FROM Subscriber WHERE who = :1', user).get()
        if sub:
            values = { 'user' : user, 'subscriber' : sub }
            self.response.out.write(template.render('../templates/settings.html', values))    
        else:
            self.redirect('/app')
            
    def post(self):
        user = users.get_current_user()
        sub = db.GqlQuery('SELECT * FROM Subscriber WHERE who = :1', user).get()
        values = { 'user' : user }
        if sub:
            sub.default_tag = self.request.get('default_tag')[:50]
            sub.mobile = self.request.get('mobile')[:50]
            sub.mobile_tag = self.request.get('mobile_tag')[:50]
            sub.nudge = self.request.get('nudge')
            if sub.nudge == 'monthly':
                sub.nudge_value = self.request.get('nudge_month_value')[:3]
            elif sub.nudge == 'weekly':
                sub.nudge_value = self.request.get('nudge_day')[:3]
            sub.put()
            values['message'] = 'Settings saved.' + sub.nudge_value
            values['message_class'] = 'success'
            values['subscriber'] = sub
            self.response.out.write(template.render('../templates/settings.html', values))
        else:
            values['message'] = 'ERROR! Subscriber not found.  Please try again.'
            values['message_class'] = 'error'
            self.response.out.write(template.render('../templates/settings.html', values))

def main():
    app = webapp.WSGIApplication([
        ('/settings', SettingsHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()