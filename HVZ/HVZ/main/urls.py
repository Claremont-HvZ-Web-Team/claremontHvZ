from django.contrib.auth.views import login, logout_then_login
from django.conf.urls import patterns, url

from views import LandingPage, Register
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('HVZ.main.views',
    # Examples:
    # url(r'^$', 'HVZ.views.home', name='home'),
    # url(r'^HVZ/', include('HVZ.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^login', login,  name="login"),
    url(r'^logout', logout_then_login, name="logout"),
    url(r'^register/', Register.as_view(), name="register"),

    url(r'^$', LandingPage.as_view(), name="main_landing"),
)
