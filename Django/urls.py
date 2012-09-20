from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Django.views.home', name='home'),
    # url(r'^Django/', include('Django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'HvZ.views.homepage_view', name='home_view'),
    url(r'^rules/$', 'HvZ.views.rules_list_view', name='rules_list'),
    url(r'^forum/$', 'HvZ.views.forum_thread_view'),
    url(r'^mission/$', 'HvZ.views.mission_list_view',),
    url(r'^status/$', 'HvZ.views.stats_down_view'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )
