#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import db


class Task(db.Model):
	name = db.StringProperty(required=True)
	who = db.UserProperty(required=True)
	when = db.DateTimeProperty(auto_now_add=True)
	nudge = db.StringProperty(required=True, choices=set(
		["never", "everyday", "tomorrow", "friday", "eom", "specific"]))
	nudged = db.BooleanProperty(default=False)
	nudge_date = db.DateTimeProperty
	complete = db.BooleanProperty()
	tags = db.StringListProperty()


class Subscriber(db.Model):
	who = db.StringProperty(required=True)
	when = db.DateTimeProperty(auto_now_add=True)