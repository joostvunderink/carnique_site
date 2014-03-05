from django.db import models
from django.contrib.auth.models import User

from carnique.utils import get_square_html, get_square_color
import datetime

class UserProfile(models.Model):
    realname  = models.TextField(blank=True)
    location  = models.TextField(blank=True)
    url       = models.URLField(blank=True)
    birthday  = models.DateField(blank=True, null=True)
    is_member = models.BooleanField()
    text      = models.TextField(blank=True)
    user      = models.ForeignKey(User, unique=True)
    twitter_username = models.CharField(max_length=50, blank=True, null=True)
    blog_url         = models.CharField(max_length=250, blank=True, null=True)
    blog_name        = models.CharField(max_length=250, blank=True, null=True)
    last_updated     = models.DateTimeField(null=True)

    def __unicode__(self):
        return "Profile of %s" % self.user.username

    def get_square_html(self):
        color = self.get_last_updated_color()
        size = 8

        # from carnique.utils
        return get_square_html(color, size)

    def get_last_updated_color(self):
        if not self.last_updated:
            return '000000';

        secs = self.get_seconds_since_update()
        return get_square_color(secs)

    def get_seconds_since_update(self):
        if not self.last_updated:
            return 10000000

        delta = datetime.datetime.now() - self.last_updated

        return 86400 * delta.days + delta.seconds

