from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   #  url(r'^$', 'presentation.views.home', name='home'),
   #   url(r'^rebelle/$', 'presentation.views.rebelle', name='rebelle'),
      url(r'^$', 'presentation.views.rebelle', name='rebelle'),

)
