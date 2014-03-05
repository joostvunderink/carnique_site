from carnique.profile.models import UserProfile
from carnique.quotes.models import Quote
from carnique.news.models import News
from django.contrib import admin

admin.site.register(News)
admin.site.register(Quote)
admin.site.register(UserProfile)

