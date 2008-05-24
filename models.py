#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import db


class Subscriber(db.Model):
	who = db.StringProperty(
		required=True)
	when = db.DateTimeProperty(
		auto_now_add=True)