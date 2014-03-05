from django.db import models
from django.contrib.auth.models import User
import datetime

class Quote(models.Model):
    title     = models.TextField(blank=True)
    text      = models.TextField(blank=True)
    score     = models.IntegerField(default=0)
    added_by  = models.ForeignKey(User)
    added_on  = models.DateField(default=datetime.datetime.now())

    def __unicode__(self):
        return "\"%s\" (%s)" % (self.title, self.added_by.username)

class QuoteVote(models.Model):
    quote     = models.ForeignKey(Quote)
    user      = models.ForeignKey(User)
    ip        = models.IPAddressField()
    ts        = models.DateTimeField()

    def __unicode__(self):
        return "Voted on %s on %s from %s" % (self.quote.id, self.ts, self.ip)
