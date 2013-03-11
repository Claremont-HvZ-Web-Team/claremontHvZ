from django import forms

from HVZ.main.forms import FeedCodeField
from HVZ.main.models import Building
from HVZ.main import validators
from HVZ.feed.validators import human_with_code


class MealForm(forms.Form):
    feedcode = FeedCodeField(
        label="Feed code",
        help_text="Type in the feed code of the person you ate",
        validators=[human_with_code],
    )

    time = forms.DateTimeField(
        required=False,
        validators=[validators.validate_past,
                    lambda t: validators.DateValidator()(t.date()),
        ]
    )

    location = forms.ModelChoiceField(
        Building.objects,
        required=False,
    )

    description = forms.CharField(
        widget=forms.Textarea,
    )
