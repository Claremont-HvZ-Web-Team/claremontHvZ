from django.conf.urls import patterns, url

from views import PlayerListView


urlpatterns = patterns('HVZ.players.views',
    url(r'^$', PlayerListView.as_view(), name='player_list'),
)
