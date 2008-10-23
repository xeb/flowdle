#!/usr/bin/env python

import os
import wsgiref.handlers

from datetime import datetime
from models import Task
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.api import mail
from google.appengine.api import urlfetch


class Common():
    def sendTask(self, task, handler):
        if task.last_nudge == None or task.last_nudge.day.__str__() != datetime.now().day.__str__() or task.last_nudge.month.__str__() != datetime.now().month.__str__() or task.last_nudge.year.__str__() != datetime.now().year.__str__():
            message = mail.EmailMessage(sender="no-reply@flowdle.com",
                  to=task.who.email(),
                  #to='xebxeb@gmail.com',
                  subject="Flowdle Nudge for: " + task.name,
                  body=task.name + "\n\n http://www.flowdle.com/")        
            message.send()
            task.last_nudge = datetime.now()
            task.put()
            return True
        else:
            return False
              
class MasterBlaster(webapp.RequestHandler):
    
    def get(self):
        query = "SELECT * FROM Subscriber"
        people = db.GqlQuery(query)
        if people:
            for person in people:
                self.response.out.write(person.who.email() + '<br/>')
                #result = urlfetch.fetch('http://localhost:8080/nudger/send?user=' + person.who.email())
                
                
class Sender(webapp.RequestHandler):
    
    def get(self):  
        user = users.User(self.request.get('user'))
        #self.response.out.write(datetime.datetime.today().day.__str__() + '<br />')
        if user:
            cmn = Common()
            query =  "SELECT * FROM Task WHERE nudge = :1 AND who = :2 AND complete = False "
            
            # Daily Tasks
            tasks = db.GqlQuery(query, 'daily', user)
            if tasks:
                for task in tasks:
                    self.response.out.write('(' + task.key().id().__str__() + ', daily) Last_Nudge was ' + task.last_nudge.__str__() + '<br />')
                    if cmn.sendTask(task, self):  
                        self.response.out.write('Sending...' + task.key().id().__str__() + ' <br />')

            # Weekly Tasks
            tasks = db.GqlQuery(query, 'weekly', user)
            if tasks:
                for task in tasks:
                    if datetime.now().isoweekday().__str__() == task.nudge_value.__str__():
                        self.response.out.write('(' + task.key().id().__str__() + ', weekly) Last_Nudge was ' + task.last_nudge.__str__() + '<br />')
                        if cmn.sendTask(task, self):
                            self.response.out.write('Sending...' + task.key().id().__str__() + '  <br />')
                            
            # Monthly Tasks
            tasks = db.GqlQuery(query, 'monthly', user)
            if tasks:
                for task in tasks:
                    if datetime.now().day.__str__() == task.nudge_value.__str__():
                        self.response.out.write('(' + task.key().id().__str__() + ', monthly) Last_Nudge was ' + task.last_nudge.__str__() + '<br />')
                        if cmn.sendTask(task, self):
                            self.response.out.write('Sending...' + task.key().id().__str__() + '  <br />')
                            
            self.response.out.write('<br /><br /><a href="/app/all">Go Back to All</a>')


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
    
    
    
    
