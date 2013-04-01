from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.conf.urls import patterns, url

from views import LandingPage, Register
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('HVZ.main.views',
    url(r'^login', login,  name="login"),
    url(r'^logout', logout_then_login, name="logout"),
    url(r'^register/', Register.as_view(), name="register"),

    # Auth versions of the above basics
    url(r'^login', login,  name="auth_login"),
    url(r'^register/', Register.as_view(), name="registration_register"),

    url(r'^user/password/reset/$',
        password_reset,
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$',
        password_reset_done),
    url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {'post_reset_redirect' : '/user/password/done/'}),
    url(r'^user/password/done/$',
        password_reset_complete),
    url(r'^$', LandingPage.as_view(), name="main_landing"),
)
