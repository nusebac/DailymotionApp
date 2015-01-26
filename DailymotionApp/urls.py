from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'Dashboard.views.home', name='home'),
     url(r'^common/', 'Dashboard.views.common', name='common'),
     url(r'^charts/', 'Dashboard.views.charts', name='charts'),
     url(r'^query/(?P<value>)', 'Dashboard.views.query', name='query'),
     url(r'^admin/', include(admin.site.urls)),
)
