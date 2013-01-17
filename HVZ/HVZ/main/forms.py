from django import forms
from django.contrib.auth.models import User
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.conf import settings

from HVZ.main import utils
from HVZ.main.models import Player, School, Building

from validators import validate_chars, feedcode_human


class FeedCodeField(forms.CharField):

    def __init__(self, *args, **kwargs):
        kwargs["min_length"] = settings.FEED_LEN
        kwargs["max_length"] = settings.FEED_LEN
        return super(FeedCodeField, self).__init__(*args, **kwargs)

    default_validators = (forms.CharField.default_validators +
                          [validate_chars])


# Help text for the widgets in the Player creation form.

CELL_TEXT = """\
If you want to be able to text message the game's website enter in your \
phone number here. We will not use this number except in emergencies or \
in response to texts from you."""

OZ_TEXT = """\
Check this box if you would like to begin afflicted with the zombie curse."""

FEED_TEXT = """\
When you are finished entering in all of your other information, have the \
tabler registering you type in your feed code. Feed codes can only contain \
the letters {}.""".format(settings.VALID_CHARS)

C3_TEXT = """\
Check this box if you would like to begin as a member of C3."""


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ["school",
                  "dorm",
                  "grad_year",
                  "cell",
                  "oz",
                  "c3",
                  "feed"]

    school = forms.ModelChoiceField(
        queryset=School.objects,
        required=True,
        empty_label="Select a school",
    )

    dorm = forms.ModelChoiceField(
        queryset=utils.dorms(),
        required=True,
        empty_label="Select a dorm",
    )

    grad_year = forms.IntegerField(required=True)

    cell = USPhoneNumberField(
        label="Cell Number",
        required=False,
        help_text=CELL_TEXT
    )

    oz = forms.BooleanField(
        label="OZ Pool",
        required=False,
        help_text=OZ_TEXT,
    )

    c3 = forms.BooleanField(
        label="C3 Pool",
        required=False,
        help_text=C3_TEXT,
    )

    feed = FeedCodeField(
        label="Feed Code",
        required=True,
        help_text=FEED_TEXT
    )

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")

    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               label="Password.")
