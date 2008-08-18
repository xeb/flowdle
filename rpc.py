# !/usr/bin/env python


import os

from django.utils import simplejson
from google.appengine.ext import webapp
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
 
  def get(self):
    func = None
   
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


class RPCMethods:
  """ Defines the methods that can be RPCed.
  NOTE: Do not allow remote callers access to private/protected "_*" methods.
  """

  def ToggleComplete(self, *args):
    return 'Cool'
    task = db.GqlQuery('SELECT * FROM Task WHERE ANCESTOR IS :1',db.Key(args[0])).get()
    if task:
        if task.complete:
            task.complete = False
        else:
            task.complete = True
        task.put()
        return True
    else:
        return False
        
 
def main():
  app = webapp.WSGIApplication([
    ('/rpcget', MainPage),
    ('/rpccmd', RPCHandler),
    ], debug=True)
  util.run_wsgi_app(app)

if __name__ == '__main__':
  main()