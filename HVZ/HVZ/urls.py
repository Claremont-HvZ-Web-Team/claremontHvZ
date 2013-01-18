from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

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

    url(r'^register/',
        permission_required("main.add_player")(
            HVZ.main.views.Register.as_view()
        ),
        name="register"),

    #  url(r'^login/', HVZ.main.views.Login.as_view()),
    url(r'^login/', 'django.contrib.auth.views.login', name="login"),

    url(r'^eat/',
        login_required(
            HVZ.feed.views.MealCreate.as_view()
        ),
        name="eat"),

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
