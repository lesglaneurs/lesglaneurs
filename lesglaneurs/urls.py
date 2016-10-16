from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

                       url(r'^local/$', 'lesglaneurs.views.home', name='home'),

                       url(r'^local/quiz_typeform/$', 'lesglaneurs.views.quiz_typeform', name='quiz'),
                       url(r'^local/presentation/', include('presentation.urls')),
                       url(r'^local/admin/', include(admin.site.urls)),
)
