from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^(?P<username>[^/]+)/$', 'carnique.profile.views.profile_view'),
    (r'^(?P<username>[^/]+)/edit/$', 'carnique.profile.views.profile_edit')
)

