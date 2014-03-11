import json

from django.http import HttpResponse

from HVZ.main.models import Player
from HVZ.main.models import Building
from django.contrib.auth.models import User


def json_get_all_graduation_years(request):
    """A pretty useless function that displays all graduation years.

    You should replace this with one you actually want.

    """

    # Check out HVZ/main/models.py for helper functions relating to Players.
    # Player.current_players() returns all Players in the current Game.
    years = Player.logged_in_player(request).team

    # json.dumps creates a string from a Python object. You can then
    # read the string and convert it into an Objective-C data
    # structure using NSJSONSerialization in Objective-C.
    json_data = json.dumps(years)

    return HttpResponse(
        json_data,
        content_type="application/json"
    )


def json_get_current_player_team(request):
    """Returns H or Z, corresponding to logged in player's team."""

    team = Player.logged_in_player(request).team
    json_data = json.dumps(team)

    return HttpResponse(
        json_data,
        content_type="application/json"
    )

def json_get_all_buildings(request):
    """Returns H or Z, corresponding to logged in player's team."""
    buildings = [ b.name for b in Building.objects.all() ]
    json_data = json.dumps(buildings)

    return HttpResponse(
        json_data,
        content_type="application/json"
    )

def json_get_current_player_name(request):
    """Returns the concatenated first and last names of the logged in player."""
    name = Player.logged_in_player(request).user.get_full_name();
    json_data = json.dumps(name);

    return HttpResponse(
        json_data,
        content_type="application/json"
    )

def json_get_human_zombie_ratio(request):
    """Returns a string describing the spread of
    the infection, in the format #humans/#zombies"""
    numHumans = Player.objects.filter(team="H").count()
    numZombies = Player.objects.filter(team="Z").count()
    info = str(numHumans) + "/" + str(numZombies)
    json_data = json.dumps(info)

    return HttpResponse(
        json_data,
        content_type="application/json"
    )
