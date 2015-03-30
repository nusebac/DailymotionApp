from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'Dashboard.views.home', name='home'),
     url(r'^common/', 'Dashboard.views.common', name='common'),
     url(r'^France/', 'Dashboard.views.France', name='France'),
     url(r'^news/', 'Dashboard.views.news', name='news'),
     url(r'^sports/', 'Dashboard.views.sports', name='sports'),
     url(r'^movies/', 'Dashboard.views.movies', name='movies'),
     url(r'^charts/', 'Dashboard.views.charts', name='charts'),
     url(r'^comedy/', 'Dashboard.views.comedy', name='comedy'),
     url(r'^celeb/', 'Dashboard.views.celeb', name='celeb'),
     url(r'^query/(?P<value>)', 'Dashboard.views.query', name='query'),
     url(r'^admin/', include(admin.site.urls)),
)
