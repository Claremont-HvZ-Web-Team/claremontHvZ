from django.conf import settings
from django.conf.urls import patterns, include, url

import HVZ.feed.views
import HVZ.main.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:

    # Coupled to settings.LOGIN_URL for reasons out of my control.
    url(r'^login/', 'django.contrib.auth.views.login', name="login"),

    url(r'^eat/', HVZ.feed.views.EatView.as_view(), name="eat"),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # anything else gets handled by the main app
    url(r'', include('HVZ.main.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url('^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.STATIC_ROOT,
                }),
        )
