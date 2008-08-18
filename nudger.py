#!/usr/bin/env python

import os
import wsgiref.handlers

from models import Task
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template


class NudgeHandler(webapp.RequestHandler):
    
    def get(self):  
        tasks = db.GqlQuery('SELECT * FROM Task WHERE complete = False')
        if tasks:
            for task in tasks:
                if task.nudge == 'daily':
                    self.response.out.write(task.name)
                    

def main():
    app = webapp.WSGIApplication(
                [
                    ('/nudger/send', NudgeHandler)
                ], 
                debug=True)
    wsgiref.handlers.CGIHandler().run(app)

    
if __name__ == "__main__":
    main()
    
    
    
    
