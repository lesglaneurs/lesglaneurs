from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', 'lesglaneurs.views.home', name='home'),
                       url(r'^quiz_typeform/$', 'lesglaneurs.views.quiz_typeform', name='quiz'),
                       url(r'^admin/', include(admin.site.urls)),
)
