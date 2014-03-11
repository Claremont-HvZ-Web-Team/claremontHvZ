from django.conf.urls import patterns, url

from HVZ.api.views import json_get_current_player_team
from HVZ.api.views import json_get_all_buildings
from HVZ.api.views import json_get_current_player_name
from HVZ.api.views import json_get_human_zombie_ratio

urlpatterns = patterns('HVZ.api.views',
    url('^team', json_get_current_player_team),
    url('^buildings', json_get_all_buildings),
    url('^fullname', json_get_current_player_name),
    url('^hvzratio', json_get_human_zombie_ratio),
)
