from django import forms
from django.conf import settings

from HVZ.main.forms import FeedCodeField
from HVZ.feed.models import Meal

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["time", "location", "description"]

    feedcode = FeedCodeField(
        help_text="Type in the feed code of the person you ate"
    )
