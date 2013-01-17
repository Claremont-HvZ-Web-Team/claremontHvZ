from datetime import datetime

from django.core.exceptions import ValidationError
from django.conf import settings

from HVZ.main import utils

def ensure_human(player):
    if player.team != "H":
        raise ValidationError("{} is not a human!".format(player))

def ensure_zombie(player):
    if player.team != "Z":
        raise ValidationError("{} is not a zombie!".format(player))
