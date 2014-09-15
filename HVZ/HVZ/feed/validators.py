from django.core.exceptions import ValidationError

from HVZ.main.models import Player


def human_with_code(feedcode):
    """Ensure the feedcode corresponds to a currently-playing Human."""
    if not Player.current_players().filter(team="H", feed=feedcode).exists():
        raise ValidationError(
            "{} doesn't correspond to a playing human!".format(feedcode))

def zombie_has_enough_meals(donatorMeals,donatorUpgrade,mealsToDonate):
	"""Ensure this zombie can donate as many meals as they claim"""
	thresholds = {'n' : 4, 'N' : 7, 'D' : 10, 'E' : 8}
	if donatorUpgrade in thresholds:
		minimumAmount = thresholds[donatorUpgrade]
	else :
		minimumAmount = 0
	if donatorMeals - mealsToDonate < minimumAmount:
		return False
	else :
		return True