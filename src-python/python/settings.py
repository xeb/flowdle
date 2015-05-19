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
            if sub.nudge_time == None:
                sub.nudge_time = "morning"
                sub.put()
            if sub.sort == None:
                sub.sort = "when"
                sub.put()
            if sub.sort_asc == None:
                sub.sort_asc = True
                sub.put()
            values = { 'user' : user, 'subscriber' : sub }
            self.response.out.write(unicode(template.render('templates/settings.html', values))) 
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
            elif sub.nudge == 'yearly':
                sub.nudge_value = self.request.get('nudge_year_value')[:6]
                
            #sub.nudge_time = self.request.get('nudge_time')
            sub.sort = self.request.get('sort')
            sub.sort_asc = self.request.get('sort_asc') != "no"
            sub.group_nudges = self.request.get('group_nudges') == "yes"
            sub.put()
            values['message'] = 'Settings saved.'
            values['message_class'] = 'success'
            values['subscriber'] = sub
            self.response.out.write(unicode(template.render('templates/settings.html', values)))
        else:
            values['message'] = 'ERROR! Subscriber not found.  Please try again.'
            values['message_class'] = 'error'
            self.response.out.write(unicode(template.render('templates/settings.html', values)))

def main():
    app = webapp.WSGIApplication([
        ('/settings', SettingsHandler)], debug=False)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()