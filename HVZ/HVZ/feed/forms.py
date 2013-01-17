from django.forms import CharField, ModelForm
from django.conf import settings

import models
from validators import feedcode_human, validate_chars

class MealForm(ModelForm):
    class Meta:
        model = models.Meal
        fields = ["time", "location", "description"]

    feedcode = models.FeedCodeField.formfield(
        help_text="Type in the feed code of the person you ate"
    )
