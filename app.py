#!/usr/bin/env python

import os
import wsgiref.handlers

from models import Task
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template


class ListPage:
    """ A Common Class for Rendering the Main Template """
    def show(self, handler):
        user = users.get_current_user()
        alltasks = db.GqlQuery( 'SELECT * FROM Task WHERE who = :1 ' 
                                ' ORDER BY when DESC ', user)
        values = {
            'user': user,
            'signout' : users.create_logout_url("/"),
            'taglist' : 'None',
            'alltasks' : alltasks,
			'formaction' : '/app'
        }

        handler.response.out.write(template.render('templates/app.html', values))   


class MainHandler(webapp.RequestHandler):
    def get(self):
        lst = ListPage()
        lst.show(self)
        
    def post(self):
        task = Task(
            name=self.request.get('taskname')[:200],
            who=users.get_current_user(),
			tags=self.request.get('taglist')[:500].split(' ')
            )
        task.put()
        self.redirect('/app')


def main():
    app = webapp.WSGIApplication(
                [
                    ('/app', MainHandler)
                ], 
                debug=True)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()