from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
                       #  url(r'^$', 'presentation.views.home', name='home'),
                       url(r'^events/$', views.events, name='events'),
                       url(r'^projects/$', views.projects, name='projects'),
                       url(r'^projects/(?P<project_id>[0-9]{1})?/$', views.projects, name='projects'),
                       url(r'^calendar.html', views.calendar, name='calendar'),
                       url(r'^map', views.map, name='map'),
                       url(r'^points', views.points, name='points'),
                       url(r'^populate', views.populate, name='populate'),
)
