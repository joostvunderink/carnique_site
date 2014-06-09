from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone
import datetime

quote_vote_expiry_time = datetime.timedelta(1, 0)

class Quote(models.Model):
    title     = models.TextField(blank=True)
    text      = models.TextField(blank=True)
    score     = models.IntegerField(default=0)
    added_by  = models.ForeignKey(User)
    added_on  = models.DateField(default=datetime.datetime.now())

    def can_vote(self):
        print "can_vote, qid = '%d'" % self.id;
        return not self._already_voted()

    def _already_voted(self):
        qvs = QuoteVote.objects.all().filter(quote=self)
        now = django.utils.timezone.now()

        for qv in qvs:
            if now - qv.ts < quote_vote_expiry_time:
                return True

        return False

    def __unicode__(self):
        return "\"%s\" (%s)" % (self.title, self.added_by.username)

class QuoteVote(models.Model):
    quote     = models.ForeignKey(Quote)
    user      = models.ForeignKey(User, null=True)
    ip        = models.IPAddressField()
    ts        = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return "Voted on %s on %s from %s" % (self.quote.id, self.ts, self.ip)
