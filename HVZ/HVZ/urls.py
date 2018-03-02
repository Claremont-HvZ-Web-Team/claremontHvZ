from django.http import HttpResponseRedirect
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#added from API urls.py
from HVZ.api.views import json_get_all_emails

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


def mobile_redirect(request, x):
    return HttpResponseRedirect('/' + x)

urlpatterns = patterns(
    '',
    # Examples:

    # Coupled to settings.LOGIN_URL for reasons out of my control.
    url(r'^login/', 'django.contrib.auth.views.login', name="login"),

    url(r'^eat/', include('HVZ.feed.urls')),
    url(r'^forum/', include('HVZ.forum.urls')),
    url(r'^rules/', include('HVZ.rules.urls')),

    url(r'^missions/', include('HVZ.missions.urls')),
    url(r'^players/', include('HVZ.players.urls')),
    url(r'^status/', include('HVZ.stats.urls')),

    url(r'^api/', include('HVZ.api.urls')),

    # mobile site does not exist. redirect to same page, hopefully with
    # responsive design shit.
    url(r'^mobile/(.*)', mobile_redirect),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # anything else gets handled by the main app
    url(r'', include('HVZ.main.urls')),

    #added from API urls.py
    url('^emails', json_get_all_emails)
)

# Serving static files in development
urlpatterns += staticfiles_urlpatterns()
