from django.conf.urls import patterns, url

from views import FullStatPage


urlpatterns = patterns('HVZ.stats.views',
    url(r'^$', FullStatPage.as_view(), name='stats_list'),
)
