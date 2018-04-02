from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.utils.safestring import mark_safe
from hvz.main import models, validators

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
                          [validators.validate_feedcode_chars])

class RegisterForm(forms.ModelForm):

    error_messages = {
        'duplicate_user': "You have already registered for this game!",
        'duplicate_feed': "That feed code is already in use for this game!",
        'password_mismatch': "The two password fields didn't match!",
    }

    first_name = forms.CharField(
        label="First name",
        required=True,
    )

    last_name = forms.CharField(
        label="Last name",
        required=True,
    )

    email = forms.EmailField(required=True)

    def clean_email(self):
        """Ensure that a user does not register twice for the same game."""
        email = self.cleaned_data['email']

        if models.Player.current_players().filter(
               Q(user__username=email) | Q(user__email=email)
           ).exists():
            raise ValidationError(self.error_messages['duplicate_user'])

        return email

    password1 = forms.CharField(
        label="Create a password",
        widget=forms.PasswordInput,
        required=True,
    )

    password2 = forms.CharField(
        label="Retype the password",
        widget=forms.PasswordInput,
        required=True,
    )

    def clean_password2(self):
        """Ensure that the two password fields match."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])

        return password2

    school = forms.ModelChoiceField(
        queryset=models.School.objects,
        required=False,
        empty_label="Select a school",
    )

    dorm = forms.ModelChoiceField(
        queryset=models.Building.dorms().order_by("name"),
        required=False,
        empty_label="Select a dorm",
    )

    grad_year = forms.IntegerField(
        label="Expected graduation year",
        required=False,
	min_value=2000,
	max_value=2100,
    )

    can_oz = forms.BooleanField(
        label="Candidate for Original Zombie",
        required=False,
    )

    feed = FeedCodeField(
        label="Enter the Feed Code on your index card (not case sensitive)",
        required=True,
    )
    waiver_box = forms.BooleanField(
        label=mark_safe('I have read and agree to the <a href='
    '"https://drive.google.com/file/d/0B78zrV_AHqA4VHJLdzRQOFpfT28/view">'
    'HvZ Waiver of Liability</a>'),
    required=True,
    )

    def clean_feed(self):
        """Ensure that the same feed code is not used twice in the same game."""
        feedcode = self.cleaned_data['feed']

        if models.Player.current_players().filter(feed=feedcode).exists():
            raise ValidationError(self.error_messages['duplicate_feed'])

        return feedcode

    class Meta:
        model = models.Player
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'school',
            'dorm',
            'grad_year',
            'can_oz',
            'feed',
            'waiver_box',
        )

    @transaction.atomic
    def save(self, commit=True):
        """Save the player, creating or updating the user if necessary."""
        player = super(RegisterForm, self).save(commit=False)

        def grab(s):
            return self.cleaned_data.get(s)

        email = grab('email')
        password = grab('password1')

        try:
            user = User.objects.select_for_update().get(username=email)
            user.set_password(password)
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                username=email,
                password=password,
            )

        user.first_name = grab("first_name")
        user.last_name = grab("last_name")
        user.full_clean()

        player.user = user
        player.game = models.Game.objects.latest()

        if commit:
            user.save()
            player.save()

        return player

def human_with_code(feedcode):
    """Ensure the feedcode corresponds to a currently-playing Human."""
    if not models.Player.current_players().filter(team="H", feed=feedcode).exists():
        raise ValidationError(
            "{} doesn't correspond to a playing human!".format(feedcode))

class MealForm(forms.Form):

    feedcode = FeedCodeField(
        label="Feed code",
        help_text="Type in the feed code of the person you ate",
        validators=[human_with_code],
    )

    description = forms.CharField(
        widget=forms.Textarea,
        required=False,
    )

    location = forms.ModelChoiceField(
        models.Building.objects,
        required=False,
    )

    def clean(self, *args, **kwargs):
        self.cleaned_data['time'] = settings.NOW()
        return self.cleaned_data

class DonateForm(forms.Form):

    receiver = forms.ModelChoiceField(
        None,
        required=True,
    )

    num_brains = forms.IntegerField(
        required=True,
        min_value=1,
        label="Number of Brains",
    )

    def __init__(self, *args, donor, **kwargs):
        super(DonateForm, self).__init__(*args, **kwargs)

        self.donor = donor
        self.fields['receiver'].queryset = (
            models.Player.current_players()
                .filter(team="Z")
                .exclude(id=donor.id)
        )
        self.fields['num_brains'].max_value = donor.brains

    def clean(self):

        cleaned_data = super(DonateForm, self).clean()
        if not 'receiver' in cleaned_data:
            raise forms.ValidationError(
                "You must specify a person to receive your brains!"
            )

        receiver = cleaned_data['receiver']

        if receiver == self.donor:
            raise forms.ValidationError("You cannot donate to yourself!")

        if receiver.team == "H":
            raise forms.ValidationError(
                "You donated brains to a Human! They don't want your brains! Yet..."
            )

        if not 'num_brains' in cleaned_data:
            raise forms.ValidationError(
                "You must specify a number of brains to donate!"
            )

        num_brains = cleaned_data['num_brains']
        if num_brains <= 0:
            raise forms.ValidationError(
                "You must donate a positive number of brains!"
            )
        if num_brains > self.donor.brains:
            raise forms.ValidationError(
                "You cannot donate more brains than you have!"
            )

        return cleaned_data

class HarrassmentForm(forms.Form):
    description = forms.CharField(
        widget=forms.Textarea,
        label="Description",
        required=True,
    )

    anonymous = forms.BooleanField(
        label="Check to send anonymously",
        required=False,
    )
