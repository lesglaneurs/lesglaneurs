from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
   #  url(r'^$', 'presentation.views.home', name='home'),
      url(r'^(?P<project_name>(.*))/$', views.project, name='project'),
      url(r'^event/(?P<event_id>(.*))/$', views.event, name='event'),
      url(r'^calendar$', views.calendar, name='calendar'),
)
