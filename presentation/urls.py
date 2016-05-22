from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'persons', views.PersonViewSet)

urlpatterns = patterns('',
                       #  url(r'^$', 'presentation.views.home', name='home'),
                       url(r'^events/$', views.events, name='events'),
                       url(r'^projects/$', views.projects, name='projects'),
                       url(r'^projects/(?P<project_id>[0-9]{1})?/$', views.projects, name='projects'),
                       url(r'^calendar.html', views.calendar, name='calendar'),
                       url(r'^map$', views.map, name='map'),
                       url(r'^map_addresses', views.map_addresses, name='map_addresses'),
                       url(r'^map_events', views.map_events, name='map_events'),
                       url(r'^empty_db', views.empty_db, name='empty_db'),
                       url(r'^load_small_data', views.load_small_data,
                           name='load_small_data'),
                       url(r'^load_big_data', views.load_big_data,
                           name='load_big_data'),

                        # Wire up REST framework API using automatic URL routing.
                        # Additionally, we include login URLs for the browsable API.
                        url(r'^', include(router.urls)),
                        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
