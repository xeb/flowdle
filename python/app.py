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
            values['tagbaseurl'] = '/app/tagged/'
            values['tagtitle'] = 'All'
            values['taglinks'] = cmn.getTagLinks(values['alltags'], None)
        
        # Show Tagged Tasks
        elif urlparam[:7] == "/tagged":
            tagstr = urlparam[8:]
            if tagstr:
                tags = [tagstr]
                values['alltasks'] = db.GqlQuery(" SELECT * FROM Task WHERE who = :1 "
                                                 " AND complete = False AND tags IN :2 "
                                                 " ORDER BY when DESC ", user, tags)
                if(values['alltasks'].count(10) == 0):
                    handler.redirect('/app/all')
                values['tagtitle'] = tagstr.title()
                values['tagdefault'] = tagstr
                values['taglinks'] = cmn.getTagLinks(values['alltags'], tags)
                values['formaction'] = '/app/tagged/' + tagstr
                values['headmenu'] = '<a href="">Nudge for all "' + tagstr + '"</a>'
            else:
                handler.redirect('/app/all')

        # Show Completed Tags
        elif urlparam == "/completed":
            values['alltasks'] = db.GqlQuery(" SELECT * FROM Task WHERE who = :1 "
                                            " AND complete = :2 ", user, True)
            values['taglinks'] = cmn.getTagLinks(values['alltags'], None)
            values['tagtitle'] = 'Completed'
            values['title'] = 'Completed Tasks will be automatically deleted after one month'
        # Show No Tag
        elif urlparam == "/notag":
            tasks = []
            for task in db.GqlQuery( "SELECT * FROM Task WHERE who = :1 " 
                                " ORDER BY when DESC ", user):
                # sigh...can't do this in GQL
                if len(task.tags) == 0:
                    tasks.append(task)
            values['alltasks'] = tasks
            values['taglinks'] = cmn.getTagLinks(values['alltags'], None)
            values['tagtitle'] = 'No Tag'

        # Send to All if Nothing has been matched
        else:
            handler.redirect('/app/all')
                
        # write out the main template to the given handler
        handler.response.out.write(template.render('../templates/app.html', values))   
        return
        
    def getTags(self, alltasks):
        taglist = []
        for task in alltasks:
            if task.tags:
                taglist.extend(task.tags)
        tagdict = sorted(list(set(taglist)), reverse=False)
        return tagdict
    
    def getTagString(self, alltags):
        tagstr = ""
        for tag in alltags:
            tagstr = tagstr + tag + " "
        return tagstr
    
    def getTagLinks(self, alltags, selected):
        taglinks = ""
        baselink = "/app/tagged/"
        for tag in alltags:
            if selected and tag in selected:
                taglinks += '<li>' + tag + '</li>'
            else:
                taglinks += '<li><a href="/app/tagged/' + tag + '">' + tag + '</a></li>'
        return taglinks
    
    def setTags(self, tagString):
        """ parses a string & returns a list of proper tags (no spaces) """
        newlist = []
        for tag in tagString[:500].split(' '):
            if tag != u' ' and tag != u'' and tag not in newlist:
                newlist.append(tag.strip()[:30])
        return newlist

        
""" Our MainHandler for /app"""
class MainHandler(webapp.RequestHandler):
    
    def get(self, urlparam):
        cmn = Common()
        cmn.showMain(self, urlparam)
        
    def post(self, urlparam):
        cmn = Common()
        task = Task(
            name=self.request.get('taskname')[:200],
            who=users.get_current_user(),
            nudge=self.request.get('nudge'))
        if self.request.get('taglist'):
            task.tags = cmn.setTags(self.request.get('taglist'))
        if self.request.get('nudge_date') and task.nudge == "specific":
            task.nudge_date = self.request.get('nudge_date')[:10]
        task.put()
        tagstr = urlparam[8:]
        if tagstr:
            self.redirect('/app/tagged/' + tagstr)
        else:
            self.redirect('/app/all')

class EditHandler(webapp.RequestHandler):
    
    def get(self, urlparam):  
        cmn = Common()  
        task = db.GqlQuery('SELECT * FROM Task WHERE ANCESTOR IS :1',db.Key(urlparam[1:])).get()
        if task:
            values = {
                'user': users.get_current_user(),
                'signout' : users.create_logout_url("/app"),        
                'name' : task.name,
                'nudge' : task.nudge,
                'tags' : cmn.getTagString(task.tags),
                'winloc' : '/app/all'
            }   
            self.response.out.write(template.render('../templates/edit.html', values)) 

    def post(self, urlparam):
        cmn = Common()
        task = db.GqlQuery('SELECT * FROM Task WHERE ANCESTOR IS :1',db.Key(urlparam[1:])).get()
        if task:
            task.name=self.request.get('taskname')[:200]            
            task.nudge=self.request.get('nudge')
            if self.request.get('taglist'):
                task.tags = cmn.setTags(self.request.get('taglist'))
            task.put()
        self.redirect('/app/all')
            
def main():
    app = webapp.WSGIApplication(
                [
                    ('/app/edit(.*)', EditHandler),
                    ('/app(.*)', MainHandler)
                ], 
                debug=True)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()
    
    
    
    
