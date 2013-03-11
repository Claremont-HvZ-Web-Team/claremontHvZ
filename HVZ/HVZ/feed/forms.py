from django import forms

from HVZ.main.forms import FeedCodeField
from HVZ.main.models import Building
from HVZ.feed.validators import human_with_code
from HVZ.feed.widgets import SelectTimeWidget

import calendar

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
