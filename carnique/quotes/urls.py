from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^$', 'carnique.quotes.views.quote_view_page'),
    (r'^(?P<quote_id>[\d]+)/$', 'carnique.quotes.views.quote_view'),
    (r'^page/(?P<page_number>[\d]+)/$', 'carnique.quotes.views.quote_view_page'),
    (r'^top/(?P<page_number>[\d]+)/$', 'carnique.quotes.views.quote_view_top_page'),
    (r'^random/$', 'carnique.quotes.views.quote_view_random'),
    (r'^add/$', 'carnique.quotes.views.quote_add'),

    (r'^(?P<quote_id>[\d]+)/vote/up/$', 'carnique.quotes.views.quote_vote_up'),
    (r'^(?P<quote_id>[\d]+)/vote/down/$', 'carnique.quotes.views.quote_vote_down'),
)

