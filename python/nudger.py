#!/usr/bin/env python

import os
import datetime
import wsgiref.handlers

from models import Task
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.api import mail
from google.appengine.api import urlfetch


class Common():
    def sendTask(self, task, handler):
        if task.last_nudge.day.__str__() == datetime.date.today().day.__str__() or task.last_nudge.month.__str__() != datetime.date.today().month.__str__() or task.last_nudge.year.__str__() != datetime.date.today().year.__str__():
            """message = mail.EmailMessage(sender="support@example.com",
                  to="xebxeb@gmail.com",
                  subject="Flowdle Nudge for: " + task.name,
                  body=task.name)        
            message.send()"""
            return True
        else:
            return False
              
class MasterBlaster(webapp.RequestHandler):
    
    def get(self):
        query = "SELECT * FROM Subscriber"
        people = db.GqlQuery(query)
        if people:
            for person in people:
                self.response.out.write('Sending to...' + person.who.email() + '<br/>')
                #result = urlfetch.fetch('http://localhost:8080/nudger/send?user=' + person.who.email())
                
                
class Sender(webapp.RequestHandler):
    
    def get(self):  
        user = users.User(self.request.get('user'))
        self.response.out.write(datetime.datetime.today().day.__str__() + '<br />')
        if user:
            cmn = Common()
            query =  " SELECT * FROM Task WHERE nudge = :1 AND who = :2 AND complete = False "
            
            # Daily Tasks
            tasks = db.GqlQuery( query, 'daily', user)
            if tasks:
                for task in tasks:
                    if cmn.sendTask(task, self):  
                        self.response.out.write('SENT DAILY')

            # Weekly Tasks
            tasks = db.GqlQuery( query, 'weekly', user)
            if tasks:
                for task in tasks:
                    if datetime.datetime.today().isoweekday().__str__() == task.nudge_value.__str__():
                        if cmn.sendTask(task, self):
                            self.response.out.write('SENT WEEKLY')
                            
            # Monthly Tasks
            tasks = db.GqlQuery( query, 'monthly', user)
            if tasks:
                for task in tasks:
                    if datetime.datetime.today().day.__str__() == task.nudge_value.__str__():
                        if cmn.sendTask(task, self):
                            self.response.out.write('SENT MONTHLY')


def main():
    app = webapp.WSGIApplication(
                [
                    ('/nudger', MasterBlaster),
                    ('/nudger/send', Sender)
                ], 
                debug=True)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()
    
    
    
    
