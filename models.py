#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import db


class Task(db.Model):
	name = db.StringProperty(required=True)
	who = db.UserProperty(required=True)
	when = db.DateTimeProperty(auto_now_add=True)
	tags = db.StringListProperty()
	complete = db.BooleanProperty(default=False)
	

class Subscriber(db.Model):
	who = db.StringProperty(required=True)
	when = db.DateTimeProperty(auto_now_add=True)
	