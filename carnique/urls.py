from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$',                           TemplateView.as_view(template_name="index.html")),
    (r'^whatiscarnique/$',            TemplateView.as_view(template_name="whatiscarnique.html")),
    (r'^guidelines/$',                TemplateView.as_view(template_name="guidelines.html")),

    url(r'^accounts/', include('django.contrib.auth.urls')),
    # (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    # (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logged_out.html', 'next_page': '/'}),
    # (r'^accounts/password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'password_edit.html'}),
    # (r'^accounts/password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'password_changed.html'}),
    # (r'^password/edit/$', 'carnique.main.views.password_edit'),

    (r'^news/',   include('carnique.news.urls')),
    (r'^quotes/', include('carnique.quotes.urls')),
    (r'^profile/', include('carnique.profile.urls')),

    (r'^todo/$', 'carnique.main.views.todo'),
    (r'^blokjes/$', 'carnique.main.views.square_test'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
