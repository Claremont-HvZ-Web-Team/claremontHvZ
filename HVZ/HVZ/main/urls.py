from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
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
