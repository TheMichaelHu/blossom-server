from google.appengine.ext import ndb

class Animation(ndb.Model):
    url = ndb.StringProperty()
    data = ndb.StringProperty()
