from django import forms

from HVZ.main.forms import FeedCodeField
from HVZ.main.models import Building, Game
from HVZ.feed.validators import human_with_code
from HVZ.feed.widgets import SelectTimeWidget

import calendar
import datetime
import time

CAL = calendar.TextCalendar(firstweekday=6)


class MealForm(forms.Form):

    feedcode = FeedCodeField(
        label="Feed code",
        help_text="Type in the feed code of the person you ate",
        validators=[human_with_code],
    )

    # given just one week to register feeds, only need to track
    # what day of week they ate.
    day = forms.ChoiceField(
        choices=(
            (i, CAL.formatweekday(i, 3)) for i in CAL.iterweekdays()
        )
    )

    time = forms.TimeField(
        required=False,
        widget=SelectTimeWidget(
            minute_step=5,
            twelve_hr=True,
        ),
    )

    location = forms.ModelChoiceField(
        Building.objects,
        required=False,
    )

    description = forms.CharField(
        widget=forms.Textarea,
    )

    def clean(self, *args, **kwargs):
        cleaned_data = super(MealForm, self).clean(*args, **kwargs)

        game_end = Game.imminent_game().end_date
        offset = (game_end.weekday() - int(cleaned_data['day']))
        feed_date = game_end - datetime.timedelta(days=offset)

        cleaned_data['day'] = feed_date

        return cleaned_data
