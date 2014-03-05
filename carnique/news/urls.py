from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^$', 'carnique.news.views.news_list'),
    (r'^add/$', 'carnique.news.views.news_add'),
)

