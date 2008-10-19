# !/usr/bin/env python


import os
import datetime
import models
from django.utils import simplejson
from models import Task
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

class MainPage(webapp.RequestHandler):
  """ Renders the main template."""
  def get(self):
    template_values = { 'title':'AJAX Add (via GET)', }
    path = os.path.join(os.path.dirname(__file__), "rpcget.html")
    self.response.out.write(template.render(path, template_values))


class RPCHandler(webapp.RequestHandler):
  """ Allows the functions defined in the RPCMethods class to be RPCed."""
  def __init__(self):
    webapp.RequestHandler.__init__(self)
    self.methods = RPCMethods()
 
  def get(self, urlparam):
    func = None
    
    #self.response.out.write('HERE')
    action = self.request.get('action')
    if action:
      if action[0] == '_':
        self.error(403) # access denied
        return
      else:
        func = getattr(self.methods, action, None)
   
    if not func:
      self.error(404) # file not found
      return
     
    args = ()
    while True:
      key = 'arg%d' % len(args)
      val = self.request.get(key)
      if val:
        args += (simplejson.loads(val),)
      else:
        break
    result = func(*args)
    self.response.out.write(simplejson.dumps(result))

class Common():
    
    def parseTags(self, tags):
        lst = ""
        for tag in tags:
            lst = lst + tag + " "
        return lst


class RPCMethods:
  """ Defines the methods that can be RPCed.
  NOTE: Do not allow remote callers access to private/protected "_*" methods.
  """


  def isRepeat(self, *args):
    cmn = Common()
    user = users.get_current_user()
    task = db.GqlQuery('SELECT * FROM Task WHERE ANCESTOR IS :1',db.Key(args[0])).get()
    if task and task.repeat == True:
        return True
    else:
        return False

  def getTask(self, *args):
    cmn = Common()
    user = users.get_current_user()
    task = db.GqlQuery('SELECT * FROM Task WHERE ANCESTOR IS :1',db.Key(args[0])).get()
    if task.complete == False and task.who == user:
        val = {
            'name' : task.name,
            'tags' : cmn.parseTags(task.tags),
            'nudge' : task.nudge,
            'nudge_value' : task.nudge_value,
            'key' : task.key().__str__(),
            'repeat' : task.repeat.__str__()
        }
        return val
    else:
        return False

  def getTaskCompleteDate(self, *args):
    user = users.get_current_user()
    task = db.GqlQuery('SELECT * FROM Task WHERE ANCESTOR IS :1',db.Key(args[0])).get()
    if task.complete == True and task.complete_date != None and task.who == user:
        val = task.complete_date.month.__str__() + '/' + task.complete_date.day.__str__() + '/' + task.complete_date.year.__str__()
        return val
    else:
        return None

  def deleteTask(self, *args):
    user = users.get_current_user()
    task = db.GqlQuery('SELECT * FROM Task WHERE ANCESTOR IS :1',db.Key(args[0])).get()
    if task:
        task.delete()
        return True
    else:
        return False
        
  def toggleComplete(self, *args):
    user = users.get_current_user()
    task = db.GqlQuery('SELECT * FROM Task WHERE ANCESTOR IS :1',db.Key(args[0])).get()
    if task and task.who == user:
        if task.complete:
            task.complete = False
        else:
            task.complete = True
            task.complete_date = datetime.datetime.today()
        task.put()
        if task.complete == True and task.repeat == True:
            # verify that we haven't repeated this already
            repeatTask = db.GqlQuery('SELECT * FROM Task WHERE who = :1 AND name = :2 AND complete = False', task.who, task.name)
            if hasattr(repeatTask, "name") == False:
                repeatTask = Task(name=task.name,
                            who=task.who,
                            tags=task.tags,
                            nudge=task.nudge,
                            nudge_value=task.nudge_value,
                            repeat=task.repeat,
                            last_nudge=task.last_nudge)
                repeatTask.put()
        return True
    else:
        return False
        
 
def main():
  app = webapp.WSGIApplication([
    ('/rpc(.*)', RPCHandler),
    ], debug=True)
  util.run_wsgi_app(app)

if __name__ == '__main__':
  main()