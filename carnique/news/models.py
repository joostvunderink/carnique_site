from django.db import models
from django.contrib.auth.models import User
import datetime
from carnique.utils import convert_bb_to_html

class News(models.Model):
    title     = models.TextField(blank=True)
    text      = models.TextField(blank=True)
    added_by  = models.ForeignKey(User)
    added_on  = models.DateField(default=datetime.datetime.now())

    def bbed_text(self):
        return convert_bb_to_html(self.text)

    def __unicode__(self):
        return "\"%s\" (%s)" % (self.title, self.added_by.username)

