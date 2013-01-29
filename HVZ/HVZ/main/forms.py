from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from HVZ.main.models import Building, Game, School
from HVZ.main.validators import validate_chars, ensure_unregistered


class PrettyAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(PrettyAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            "placeholder": "username",
        })
        self.fields['password'].widget.attrs.update({
            "placeholder": "password",
        })


class FeedCodeField(forms.CharField):

    def __init__(self, *args, **kwargs):
        kwargs["min_length"] = settings.FEED_LEN
        kwargs["max_length"] = settings.FEED_LEN
        return super(FeedCodeField, self).__init__(*args, **kwargs)

    def clean(self, value):
        return super(FeedCodeField, self).clean(value.upper())

    default_validators = (forms.CharField.default_validators +
                          [validate_chars])


class RegisterForm(forms.Form):

    first_name = forms.CharField(
        label=_("First name"),
        required=True
    )

    last_name = forms.CharField(
        label=_("Last name"),
        required=True
    )

    email = forms.EmailField(required=True, validators=[ensure_unregistered])

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        required=True
    )

    password2 = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput,
        required=True,
        help_text=_("Enter the same password as above, for verification."),
    )

    school = forms.ModelChoiceField(
        queryset=School.objects,
        required=True,
        empty_label=_("Select a school"),
    )

    dorm = forms.ModelChoiceField(
        queryset=Building.dorms(),
        required=True,
        empty_label=_("Select a dorm"),
    )

    grad_year = forms.IntegerField(required=True)

    cell = USPhoneNumberField(
        label=_("Cell Number"),
        required=False,
        help_text=_("If you want to be able to text message the game's website "
                    "enter in your phone number here. We will not use this "
                    "number except in response to texts from you.")
    )

    can_oz = forms.BooleanField(
        label=_("OZ Pool"),
        required=False,
        help_text=_("Check this box if you would like to begin afflicted with "
                    "the zombie curse.")
    )

    can_c3 = forms.BooleanField(
        label=_("C3 Pool"),
        required=False,
        help_text=_("Check this box if you would like to begin as a member of "
                    "C3.")
    )

    feed = FeedCodeField(
        label="Feed Code",
        required=True,
        help_text=_("When you are finished entering in all of your other "
                    "information, have the tabler registering you type in your "
                    "feed code. Feed codes can only contain the letters {}."
                    ).format(settings.VALID_CHARS)
    )

    def clean(self):
        if not Game.game_in_progress():
            raise ValidationError("There are no ongoing Games in progress!")

        return super(RegisterForm, self).clean()
