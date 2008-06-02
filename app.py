#!/usr/bin/env python

import os
import wsgiref.handlers

from models import Task
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template


""" Displays the Main template """
class Common:
    """ Displays the Main template """
    def showMain(self, handler):
        user = users.get_current_user()
        alltasks = db.GqlQuery( "SELECT * FROM Task WHERE who = :1 " 
                                " ORDER BY when DESC ", user)
        values = {
            'user': user,
            'signout' : users.create_logout_url("/"),
            'taglist' : 'None',
            'alltasks' : alltasks,
            'formaction' : '/app'
        }

        tags = None
        tagstr = handler.request.get('tags')
        if tagstr:
            tags = tagstr[:500].split(',')
            handler.response.out.write(tags)

        # write out the main template to the given handler
        handler.response.out.write(template.render('templates/app.html', values))   
        return
    
    def setTags(self, tagString):
        """ parses a string & returns a list of proper tags (no spaces) """
        newlist = []
        for tag in tagString[:500].split(' '):
            if tag != u' ' and tag != u'':
                newlist.append(tag.strip())
        return newlist
        
        

class MainHandler(webapp.RequestHandler):
    
    def get(self):
        cmn = Common()
        cmn.showMain(self)
        
    def post(self):
        cmn = Common()
        task = Task(
            name=self.request.get('taskname')[:200],
            who=users.get_current_user())
        # apply Tags if necessary...
        if self.request.get('taglist'):
            task.tags = cmn.setTags(self.request.get('taglist'))
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