import datetime

from django import forms

from HVZ.main.forms import FeedCodeField
from HVZ.main.models import Building
from HVZ.main.validators import TimeValidator
from HVZ.feed.validators import human_with_code


class MealForm(forms.Form):
    feedcode = FeedCodeField(
        label="Feed code",
        help_text="Type in the feed code of the person you ate",
        validators=[human_with_code],
    )

    time = forms.DateTimeField(
        required=False,
        initial=datetime.datetime.now,
        validators=[TimeValidator()],
        widget=forms.SplitDateTimeWidget,
    )

    location = forms.ModelChoiceField(
        Building.objects,
        required=False,
    )

    description = forms.CharField(
        widget=forms.Textarea,
    )
