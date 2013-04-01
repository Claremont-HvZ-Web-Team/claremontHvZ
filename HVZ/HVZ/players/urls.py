from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required

from views import PlayerListView, PlayerEmailView


urlpatterns = patterns('HVZ.players.views',
    url(r'^$', PlayerListView.as_view(), name='player_list'),
    url(r'^emailset$', staff_member_required(PlayerEmailView.as_view())),
)
