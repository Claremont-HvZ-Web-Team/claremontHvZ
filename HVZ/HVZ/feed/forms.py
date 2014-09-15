import calendar
import datetime

from django import forms
from django.conf import settings

from HVZ.main.forms import FeedCodeField
from HVZ.main.models import Building, Game, Player
from HVZ.feed.validators import human_with_code, zombie_has_enough_meals
from HVZ.feed.widgets import SelectTimeWidget

CAL = calendar.TextCalendar(firstweekday=6)


def get_offset():
    """Return the number of days since game start."""
    try:
        g = Game.imminent_game()
    except Game.DoesNotExist:
        return 0
    return (settings.NOW().date() - g.start_date).days

def get_nearest_hour():
    now = settings.NOW()
    return datetime.datetime(
        now.year, now.month, now.day,
        now.hour,
    )

def weekday_choices():
    """Returns a list of offsets from the start of the current game."""
    try:
        g = Game.imminent_game()
    except Game.DoesNotExist:
        return [(i, CAL.formatweekday(i, 3)) for i in xrange(7)]

    # Bounds on when the meal can have occurred
    start = g.start_date
    end = min(settings.NOW().date(), g.end_date)

    return (
        (i, CAL.formatweekday((start+datetime.timedelta(days=i)).weekday(), 3))
        for i in range((end-start).days+1)
    )


class MealForm(forms.Form):

    feedcode = FeedCodeField(
        label="Feed code",
        help_text="Type in the feed code of the person you ate",
        validators=[human_with_code],
    )

    # given just one week to register feeds, only need to track
    # what day of week they ate.
    day = forms.ChoiceField(
        choices=weekday_choices(),
        initial=get_offset
    )

    time = forms.TimeField(
        required=True,
        widget=SelectTimeWidget(
            minute_step=5,
            twelve_hr=True,
        ),
        initial=get_nearest_hour,
    )

    location = forms.ModelChoiceField(
        Building.objects,
        required=False,
    )

    description = forms.CharField(
        widget=forms.Textarea,
        required=False,
    )

    def clean(self, *args, **kwargs):
        cleaned_data = super(MealForm, self).clean(*args, **kwargs)

        g = Game.imminent_game()

        # Check that day and time exist
        if not 'day' in cleaned_data:
            raise forms.ValidationError("Somehow you didn't specify the day.")

        if not 'time' in cleaned_data:
            raise forms.ValidationError("Somehow you didn't select a time.")

        feed_date = g.start_date + datetime.timedelta(days=int(cleaned_data['day']))

        if feed_date < g.start_date:
            raise forms.ValidationError("Can't have eaten before the game!")

        if feed_date > g.end_date:
            raise forms.ValidationError("Can't have eaten after the game ended!")

        feed_time = datetime.datetime.combine(feed_date, cleaned_data['time'])

        if feed_time > settings.NOW():
            raise forms.ValidationError("You can't eat in the future, bro.")

        cleaned_data['time'] = feed_time
        return cleaned_data

class DonateForm(forms.Form):

    receiver = forms.ModelChoiceField(
        Player.objects.filter(team="Z"),
        required=True
        )

    numberOfMeals = forms.IntegerField(
        required=True,
        label="Number of Brains",
        )

    donatorMeals = forms.IntegerField(
        required=False,
        label="",
        )

    donatorUpgrade = forms.CharField(
        required=False,
        label="",
        )

    def clean(self, *args, **kwargs):
        cleaned_data = super(DonateForm, self).clean(*args, **kwargs)
        print cleaned_data
        if not 'receiver' in cleaned_data:
            raise forms.ValidationError("You must specify a person to receive your brains!")

        if not 'numberOfMeals' in cleaned_data:
            raise forms.ValidationError("You must specify a number of brains to donate!")

        receivingPlayer = cleaned_data['receiver']

        if not receivingPlayer.team == "Z":
            raise forms.ValidationError("You somehow donated brains to a Human! They don't want your brains! Yet...")

        num_meals = cleaned_data['numberOfMeals']
        if num_meals <= 0:
            raise forms.ValidationError("You must donate a positive number of brains!")

        donatorMeals = cleaned_data['donatorMeals']
        donatorUpgrade = cleaned_data['donatorUpgrade']
        if not zombie_has_enough_meals(donatorMeals,donatorUpgrade,num_meals):
            raise forms.ValidationError("You don't have enough brains!")

        
        return cleaned_data