from django import forms
from django.conf import settings

from HVZ.main import utils
from HVZ.main.forms import FeedCodeField
from HVZ.main.models import Building
from HVZ.feed.models import Meal
from HVZ.feed.validators import human_with_code

class MealForm(forms.Form):

    feedcode = FeedCodeField(
        help_text="Type in the feed code of the person you ate",
        validators=[human_with_code]
    )

    time = forms.DateTimeField(
        input_formats=["%a %b %d %H:%M"],
        required=False
    )

    location = forms.ModelChoiceField(
        Building.objects,
        required=False
    )

    description = forms.CharField(
        widget=forms.Textarea
    )
