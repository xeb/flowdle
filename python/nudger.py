#!/usr/bin/env python

import os
import wsgiref.handlers

from sets import Set
from datetime import datetime
from models import Task
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.api import mail
from google.appengine.api import urlfetch


class Common():
    def sendGroupTasks(self, tasks, sub, handler):
        bodytext = ""
        mobilebody = ""
        tasks_to_remove = Set([])
        
        for task in tasks:
            if task.last_nudge != None and task.last_nudge.day.__str__() == datetime.now().day.__str__() and task.last_nudge.month.__str__() == datetime.now().month.__str__() and task.last_nudge.year.__str__() == datetime.now().year.__str__():
                tasks_to_remove.add(task)
            else:
                bodytext = bodytext + task.name + "\n\n"
                task.last_nudge = datetime.now()
                task.put()
                
                if sub and sub.mobile and ( sub.mobile_tag == None or sub.mobile_tag == '' or ( sub.mobile_tag in task.tags ) ):
                    mobilebody = mobilebody + task.name + "\n\n"
        
        if len(tasks_to_remove) > 0:
            for task in tasks_to_remove:
                tasks.remove(task)
        
        #send the message
        if len(tasks) > 0:
            message = mail.EmailMessage(sender="no-reply@flowdle.com",
                to=task.who.email(),
                #to="xebxeb@gmail.com",
                subject="Flowdle Nudges (" + datetime.now().month.__str__() + "/" + datetime.now().day.__str__() + "/" + datetime.now().year.__str__() + ")",
                body=bodytext + "\n\n http://www.flowdle.com/")        
            message.send()
            
            if len(mobilebody) > 0:
                message = mail.EmailMessage(sender="no-reply@flowdle.com",
                    to=sub.mobile,
                    subject="Flowdle Nudges (" + datetime.now().month.__str__() + "/" + datetime.now().day.__str__() + "/" + datetime.now().year.__str__() + ")",
                    body=mobilebody + "\n\n http://www.flowdle.com/")        
                message.send()
            
            return True
        else:
            return False
        
        
    def sendSingleTask(self, task, sub, handler):
        # if hasn't been sent today...
        if task.last_nudge == None or task.last_nudge.day.__str__() != datetime.now().day.__str__() or task.last_nudge.month.__str__() != datetime.now().month.__str__() or task.last_nudge.year.__str__() != datetime.now().year.__str__():
            message = mail.EmailMessage(sender="no-reply@flowdle.com",
                  to=task.who.email(),
                  subject="Flowdle Nudge: " + task.name,
                  body=task.name + "\n\n http://www.flowdle.com/")        
            message.send()
            
            # send to mobile ?
            if sub and sub.mobile and ( sub.mobile_tag == None or sub.mobile_tag == '' or ( sub.mobile_tag in task.tags ) ):
                handler.response.out.write('MOBILE!!!')
                message = mail.EmailMessage(sender="no-reply@flowdle.com",
                    to=sub.mobile,
                    subject="Flowdle Nudge",
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

class Sender(webapp.RequestHandler):
    
    def get(self):  
        user = users.User(self.request.get('user'))
        sub = db.GqlQuery("SELECT * FROM Subscriber WHERE who = :1", user).get()
        #sub.group_nudges = False
        tasks_to_nudge = Set([])
        
        if user and sub:
            cmn = Common()
            query =  "SELECT * FROM Task WHERE nudge = :1 AND who = :2 AND complete = False "
            
            # Daily Tasks
            tasks = db.GqlQuery(query, 'daily', user)
            if tasks:
                for task in tasks:
                    self.response.out.write('(' + task.key().id().__str__() + ', daily) Last_Nudge was ' + task.last_nudge.__str__() + '<br />')
                    if sub.group_nudges:
                        tasks_to_nudge.add(task)
                    else:
                        if cmn.sendSingleTask(task, sub, self):  
                            self.response.out.write('Sent...' + task.key().id().__str__() + ' <br />')

            # Weekly Tasks
            tasks = db.GqlQuery(query, 'weekly', user)
            if tasks:
                for task in tasks:
                    if datetime.now().isoweekday().__str__() == task.nudge_value.__str__():
                        self.response.out.write('(' + task.key().id().__str__() + ', weekly) Last_Nudge was ' + task.last_nudge.__str__() + '<br />')
                        if sub.group_nudges:
                            tasks_to_nudge.add(task)
                        else:
                            if cmn.sendSingleTask(task, sub, self):
                                self.response.out.write('Sent...' + task.key().id().__str__() + '  <br />')
                            
            # Monthly Tasks
            tasks = db.GqlQuery(query, 'monthly', user)
            if tasks:
                for task in tasks:
                    if datetime.now().day.__str__() == task.nudge_value.__str__():
                        self.response.out.write('(' + task.key().id().__str__() + ', monthly) Last_Nudge was ' + task.last_nudge.__str__() + '<br />')
                        if sub.group_nudges:
                            tasks_to_nudge.add(task)
                        else:
                            if cmn.sendSingleTask(task, sub, self):
                                self.response.out.write('Sent...' + task.key().id().__str__() + '  <br />')

            # Yearly Tasks
            tasks = db.GqlQuery(query, 'yearly', user)
            if tasks:
                for task in tasks:
                    nudgeDay = task.nudge_value.__str__()[3:5]
                    nudgeMonth = task.nudge_value.__str__()[:2]

                    # strip leading 0s
                    if nudgeDay[:1] == '0':
                        nudgeDay = nudgeDay[1:2]
                    if nudgeMonth[:1] == '0':
                        nudgeMonth = nudgeMonth[1:2]
                    
                    if datetime.now().day.__str__() == nudgeDay.__str__() and datetime.now().month.__str__() == nudgeMonth.__str__():
                        self.response.out.write('(' + task.key().id().__str__() + ', monthly) Last_Nudge was ' + task.last_nudge.__str__() + '<br />')
                        if sub.group_nudges:
                            tasks_to_nudge.add(task)
                        else:
                            if cmn.sendSingleTask(task, sub, self):
                                self.response.out.write('Sent...' + task.key().id().__str__() + '  <br />')
            
            
            
            if sub.group_nudges and cmn.sendGroupTasks(tasks_to_nudge, sub, self):
                self.response.out.write('Sent a group Nudge...with ' + len(tasks_to_nudge).__str__() + ' tasks. <br />')


def main():
    app = webapp.WSGIApplication(
                [
                    ('/nudger', MasterBlaster),
                    ('/nudger/send', Sender)
                ], 
                debug=False)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()
    
    
    
    
