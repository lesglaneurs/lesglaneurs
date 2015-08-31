from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'lesglaneurs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^$', include('test_page.urls')),
#    url(r'^test_page/', include('test_page.urls')),
## test_page
#    url(r'^$', 'home'),
#                        url(r'^quiz_typeform/', 'quiz_typeform'),
#                        url(r'^home/', 'home'),

    url(r'^admin/', include(admin.site.urls)),
)
