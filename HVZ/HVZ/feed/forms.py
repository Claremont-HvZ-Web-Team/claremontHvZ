from django.core.exceptions import ValidationError
from django.db.models import DateTimeField
from django.forms import ModelForm

from HVZ.main.validators import TimeValidator
from HVZ.main.utils import current_game

from models import Meal
from fields import FeedCodeField
from validators import feedcode_human

class MealForm(ModelForm):
    feedcode = FeedCodeField(
        help_text="Type in the feed code of the person you ate",
        validators=FeedCodeField.default_validators+[feedcode_human]
    )

    def clean(self):
        TimeValidator()(time)
        return super(MealForm, self).clean()

    class Meta:
        model = Meal
        fields = ["time", "location", "description"]
