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
    # url(r'^$', 'HVZ.views.home', name='home'),
    # url(r'^HVZ/', include('HVZ.foo.urls')),

    url(r'^eat/', HVZ.feed.views.MealCreate.as_view()),
    url(r'^register/', HVZ.main.views.Signup.as_view()),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url('^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.STATIC_ROOT,
                }),
        )
