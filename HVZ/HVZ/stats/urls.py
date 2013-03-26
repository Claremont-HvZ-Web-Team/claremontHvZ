from django.conf.urls import patterns, url

from views import FullStatPage, JSONPlayerStats


urlpatterns = patterns('HVZ.stats.views',
    url(r'^$', FullStatPage.as_view(), name='stats_list'),
    url(r'^json/players', JSONPlayerStats.as_view(), name="stats_players"),
)
