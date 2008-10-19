#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import db


class Task(db.Expando):
    name = db.StringProperty(required=True)
    who = db.UserProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
    tags = db.StringListProperty()
    complete = db.BooleanProperty(default=False)
    complete_date = db.DateTimeProperty()
    nudge = db.StringProperty(required=True, choices=set(["never", "daily", "weekly", "monthly","yearly"]))
    nudge_value = db.StringProperty()
    last_nudge = db.DateTimeProperty()
    repeat = db.BooleanProperty(default=False)
    
    
class Subscriber(db.Model):
    who = db.UserProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
    
    
class BetaRequest(db.Model):
    who = db.StringProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
    