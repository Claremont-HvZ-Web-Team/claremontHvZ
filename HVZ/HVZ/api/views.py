import json

from django.http import HttpResponse

from HVZ.main.models import Player

def json_get_all_emails(request):
    """A pretty useless function that displays all graduation years.

    You should replace this with one you actually want.

    """

    # Check out HVZ/main/models.py for helper functions relating to Players.
    # Player.current_players() returns all Players in the current Game.
    emails = [p.user.email for p in Player.current_players()]

    # json.dumps creates a string from a Python object. You can then
    # read the string and convert it into an Objective-C data
    # structure using NSJSONSerialization in Objective-C.
    json_data = json.dumps(emails)

    return HttpResponse(
        json_data,
        content_type="application/json"
    )
