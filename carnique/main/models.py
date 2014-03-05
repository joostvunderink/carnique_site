from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

#class Quote(models.Model):
#    title     = models.TextField(blank=True)
#    text      = models.TextField(blank=True)
#    added_by  = models.ForeignKey(User)
#    added_on  = models.DateField(default=datetime.datetime.now())
#
#    def __unicode__(self):
#        return "\"%s\" (%s)" % (self.title, self.added_by.username)

#class News(models.Model):
#    title     = models.TextField(blank=True)
#    text      = models.TextField(blank=True)
#    added_by  = models.ForeignKey(User)
#    added_on  = models.DateField(default=datetime.datetime.now())
#
#    def __unicode__(self):
#        return "\"%s\" (%s)" % (self.title, self.added_by.username)

#class UserProfile(models.Model):
#    realname  = models.TextField(blank=True)
#    location  = models.TextField(blank=True)
#    url       = models.URLField(blank=True)
#    birthday  = models.DateField(blank=True, null=True)
#    is_member = models.BooleanField()
#    text      = models.TextField(blank=True)
#    user      = models.ForeignKey(User, unique=True)
#
#    def __unicode__(self):
#        return "Profile of %s" % self.user.username
#

