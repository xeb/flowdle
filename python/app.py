#!/usr/bin/env python

import os
import re
import datetime
import wsgiref.handlers
from models import Task
from models import Subscriber
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
        
        orderBy = "when"
        if handler.request.get('s') == "1":
            orderBy = "name"
        elif handler.request.get('s') == "2":
            orderBy = "nudge"
            
        orderDir = "ASC"
        if handler.request.get('o') == "1":
            orderDir = "DESC"
        
        alltasks = db.GqlQuery( "SELECT * FROM Task WHERE who = :1 AND complete = False" 
                                " ORDER BY "+orderBy+" "+orderDir, user)
        values = {
            'user': user,
            'alltasks' : alltasks,
            'alltags' : cmn.getTags(alltasks),
            'orderDir' : orderDir
        }
        
        # Show All Tasks
        if urlparam == "/all":
            values['formaction'] = '/app/all'
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
                                                 " ORDER BY "+orderBy+" "+orderDir, user, tags)
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
                                            " AND complete = :2 ORDER BY "+orderBy+" "+orderDir,
                                            user, True)
            values['taglinks'] = cmn.getTagLinks(values['alltags'], None)
            values['tagtitle'] = 'Completed'
            
            if values['alltasks'].count(1) > 0:
                values['title'] = 'Completed Tasks will be automatically deleted after one month'
                
        # Show No Tag
        elif urlparam == "/notag":
            tasks = []
            for task in db.GqlQuery( "SELECT * FROM Task WHERE who = :1 " 
                                " ORDER BY " + orderBy + " "+orderDir, user):
                # sigh...can't do this in GQL
                if len(task.tags) == 0:
                    tasks.append(task)
            values['alltasks'] = tasks
            values['taglinks'] = cmn.getTagLinks(values['alltags'], None)
            values['tagtitle'] = 'No Tag'

        # Send to All if Nothing has been matched
        else:
            handler.redirect('/app/all')
        
        # Do we have a Task        
        values['hastasks'] = values['alltasks'].count(2) > 1
                
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

    def strip_tags(self, value):
        """Return the given HTML with all tags stripped."""
        return re.sub(r'<[^>]*?>', '', value) 
        
""" Our MainHandler for /app"""
class MainHandler(webapp.RequestHandler):
    
    def get(self, urlparam):
        cmn = Common()
        user = users.get_current_user()

        # create a subscriber...
        numUsers = db.GqlQuery('SELECT * FROM Subscriber WHERE who = :1', user).count(3)
        if numUsers == 0:
            sub = Subscriber(who=user)
            sub.put()
            #self.response.out.write('Creating...')
        
        cmn.showMain(self, urlparam)
        
    def post(self, urlparam):
        cmn = Common()
        user = users.get_current_user()
        
        taskkey = len(str(self.request.get('taskkey')))
        if taskkey > 0:
            task = db.GqlQuery('SELECT * FROM Task WHERE ANCESTOR IS :1 AND who = :2',
                                    db.Key(self.request.get('taskkey')), user).get()
            if task == None:
                self.redirect('/app/all')
            else:
                task.name = cmn.strip_tags(self.request.get('taskname')[:200])
                task.nudge = self.request.get('nudge')
                task.when = datetime.datetime.today()
        else:
            task = Task(
                name=cmn.strip_tags(self.request.get('taskname')[:200]),
                who=user,
                nudge=self.request.get('nudge'))
        
        if self.request.get('taglist'):
            task.tags = cmn.setTags(self.request.get('taglist'))
          
        if task.nudge == 'monthly':
            task.nudge_value = self.request.get('nudge_month_value')[:3]
        elif task.nudge == 'weekly':
            task.nudge_value = self.request.get('nudge_day')[:3]
        
        if self.request.get('repeat') == 'True':
            task.repeat = True
        else:
            task.repeat = False
        
        #task.last_nudge = datetime.datetime.today()
        
        task.put()
        
        tagstr = urlparam[8:]
        if tagstr:
            self.redirect('/app/tagged/' + tagstr)
        else:
            self.redirect('/app/all')
            
def main():
    app = webapp.WSGIApplication(
                [('/app(.*)', MainHandler)], 
                debug=True)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()
    
    
    
    
