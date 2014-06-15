from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^$', 'carnique.quotes.views.quotes_view'),

    (r'^(?P<quote_id>[\d]+)/$', 'carnique.quotes.views.quote_view'),

    (r'^random/$', 'carnique.quotes.views.quote_view_random'),
    
    # (r'^search/$', 'carnique.quotes.views.quote_view_search'),
    (r'^add/$', 'carnique.quotes.views.quote_add'),

    # jquery interactive vote
    (r'^vote/$', 'carnique.quotes.views.quote_vote'),
)

