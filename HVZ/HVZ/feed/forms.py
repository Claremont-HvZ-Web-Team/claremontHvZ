from django.core.exceptions import ValidationError
from django.db.models import DateTimeField
from django.forms import ModelForm

from HVZ.main.validators import TimeValidator
from HVZ.feed.validators import feedcode_exists

from models import Meal
from fields import FeedCodeField

class MealForm(Form):
    class Meta:
        model = Meal
        fields = ["feed_code", "time", "location", "description"]

    feedcode = FeedCodeField(
        label='Feed Code',
        help_text="Type in the feed code of the person you ate",
        validators=FeedCodeField.default_validators+[feedcode_human]
    )

    time = DateTimeField(validators=[TimeValidator(current_game())])
