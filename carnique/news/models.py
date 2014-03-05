from django.db import models
from django.contrib.auth.models import User
import datetime

class News(models.Model):
    title     = models.TextField(blank=True)
    text      = models.TextField(blank=True)
    added_by  = models.ForeignKey(User)
    added_on  = models.DateField(default=datetime.datetime.now())

    def __unicode__(self):
        return "\"%s\" (%s)" % (self.title, self.added_by.username)

