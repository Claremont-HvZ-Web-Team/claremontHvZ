from django.conf.urls import patterns, url

from views import EatView, DonateView
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('HVZ.feed.views',
    # Examples:
    # url(r'^$', 'HVZ.views.home', name='home'),
    # url(r'^HVZ/', include('HVZ.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<feedcode>[A-Z]+)?$', EatView.as_view(), name="feed_eat"),
    url(r'^donate/', DonateView.as_view(), name="feed_donate"),
)
