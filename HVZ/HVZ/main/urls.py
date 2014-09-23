from django.contrib.auth.views import (
    login, logout_then_login, password_reset, password_reset_done,
    password_reset_confirm, password_reset_complete
)
from django.conf.urls import patterns, url

from views import LandingPage, Register, TwilioCallHandler, success, HarrassmentView, harrassmentConfirmation

urlpatterns = patterns('HVZ.main.views',
    url(r'^login', login,  name="login"),
    url(r'^logout', logout_then_login, name="logout"),
    url(r'^register/', Register.as_view(), name="register"),
    url(r'^success/', success, name="success"),
    url(r'^harrassmentForm/', HarrassmentView.as_view(), name="harrassmentForm"),
    url(r'^harrassmentConfirmation/', harrassmentConfirmation, name="harrassmentConfirmation"),

    # Auth versions of the above basics
    url(r'^login', login,  name="auth_login"),
    url(r'^register/', success, name="registration_register"),


    url(r'^user/password/reset/$',
        password_reset,
        {'post_reset_redirect': '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$',
        password_reset_done),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        password_reset_confirm,
        {'post_reset_redirect': '/user/password/done/'}),
    url(r'^user/password/done/$',
        password_reset_complete),
    url(r'^twilio/call$', TwilioCallHandler.as_view(), name="main_twilio_call"),
    url(r'^$', LandingPage.as_view(), name="main_landing"),
)
