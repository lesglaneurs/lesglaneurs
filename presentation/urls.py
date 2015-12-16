from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = patterns('',
   #  url(r'^$', 'presentation.views.home', name='home'),
   #   url(r'^rebelle/$', 'presentation.views.rebelle', name='rebelle'),

# lesglaneurs.com/presentation/rebelle.html
# lesglaneurs.com/presentation/bocal_local.html

      #url(r'^rebelle/$', 'presentation.views.rebelle', name='rebelle'),
      #url(r'^bocal_local/$', 'presentation.views.bocal_local', name='bocal_local'),

      url(r'^(?P<project_name>(.*))/$', views.project, name='project'),
)
