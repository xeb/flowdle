#!/usr/bin/env python

import os
import wsgiref.handlers

from models import Task
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template


""" Holds Common mehtods """
class Common:
    """ Displays the Main template """
    def showMain(self, handler, urlparam):
        cmn = Common()
        user = users.get_current_user()
        alltasks = db.GqlQuery( "SELECT * FROM Task WHERE who = :1 AND complete = False" 
                                " ORDER BY when DESC ", user)
        values = {
            'user': user,
            'signout' : users.create_logout_url("/app"),
            'alltasks' : alltasks,
            'alltags' : cmn.getTags(alltasks)
        }
        
        # Show All Tasks
        if urlparam == "/all":
                values['formaction'] = '/app'
                values['tagbaseurl'] = '/app?tags='
                values['tagtitle'] = 'All'
        
        # Show Tagged Tasks
        elif urlparam == "/tagged":
            tagstr = handler.request.get('tags')[:200]
            if tagstr:
                tags = tagstr.split(',')
                values['tagtitle'] = 'tags'
                values['alltasks'] = db.GqlQuery(" SELECT * FROM Task WHERE who = :1 AND tags IN :2 "
                                                 " ORDER BY when DESC ", user, tags)
                values['formaction'] = '/app?tags=' + tagstr
                values['tagbaseurl'] = '/app?tags=' + tagstr
            else:
                handler.redirect('/app/all')
                
        # Show Tagless Tags
        elif urlparam == "/tagless":
                tasks = []
                for task in db.GqlQuery( "SELECT * FROM Task WHERE who = :1 " 
                                " ORDER BY when DESC ", user):
                    if len(task.tags) == 0:
                        tasks.append(task)
                values['alltasks'] = tasks
                values['tagtitle'] = 'Tagless'

        # write out the main template to the given handler
        handler.response.out.write(template.render('templates/app.html', values))   
        return
        
    def getTags(self, alltasks):
        taglist = []
        for task in alltasks:
            if task.tags:
                taglist.extend(task.tags)
        tagdict = sorted(list(set(taglist)), reverse=False)
        #for tagkey in tagdict.keys():
        #    tagdict[tagkey] = 'test'
        return tagdict
    
    def setTags(self, tagString):
        """ parses a string & returns a list of proper tags (no spaces) """
        newlist = []
        for tag in tagString[:500].split(' '):
            if tag != u' ' and tag != u'':
                newlist.append(tag.strip())
        return newlist

        
""" Our MainHandler for /app"""
class MainHandler(webapp.RequestHandler):
    
    def get(self, urlparam):
        cmn = Common()
        cmn.showMain(self, urlparam)
        
    def post(self):
        cmn = Common()
        task = Task(
            name=self.request.get('taskname')[:200],
            who=users.get_current_user())
        # apply Tags if necessary...
        if self.request.get('taglist'):
            task.tags = cmn.setTags(self.request.get('taglist'))
        task.put()
        tagstr = self.request.get('tags')[:200]
        if tagstr:
            self.redirect('/app?tags=' + tagstr)
        else:
            self.redirect('/app')


def main():
    app = webapp.WSGIApplication(
                [
                    ('/app(.*)', MainHandler)
                ], 
                debug=True)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()
    
    
    
    
