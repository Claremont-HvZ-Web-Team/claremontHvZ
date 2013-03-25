from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django_localflavor_us.forms import USPhoneNumberField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from HVZ.main.models import Building, Game, School, Player
from HVZ.main.validators import validate_chars


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


class RegisterForm(forms.ModelForm):

    error_messages = {
        'duplicate_user': _("You have already registered for this game!"),
        'duplicate_feed': _("That feed code is already in use for this game!"),
        'password_mismatch': _("The two password fields didn't match!"),
    }

    first_name = forms.CharField(
        label=_("First name"),
        required=True
    )

    last_name = forms.CharField(
        label=_("Last name"),
        required=True
    )

    email = forms.EmailField(required=True)

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

    feed = FeedCodeField(
        label="Feed Code",
        required=True,
        help_text=_("When you are finished entering in all of your other "
                    "information, have the tabler registering you type in your "
                    "feed code. Feed codes can only contain the letters {}."
                    ).format(settings.VALID_CHARS)
    )

    class Meta:
        model = Player
        fields = ('first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2',
                  'school',
                  'dorm',
                  'grad_year',
                  'cell',
                  'can_oz',
                  'can_c3',
                  'feed',
        )

    def clean_email(self):
        """Ensure that a user does not register twice for the same game."""
        email = self.cleaned_data['email']

        if Player.current_players().filter(user__username=email).exists():
            raise ValidationError(self.error_messages['duplicate_user'])

        return email

    def clean_feed(self):
        """Ensure that the same feed code is not used twice in the same game."""
        feedcode = self.cleaned_data['feed']

        if Player.current_players().filter(feed=feedcode).exists():
            raise ValidationError(self.error_messages['duplicate_feed'])

        return feedcode

    def clean_password2(self):
        """Ensure that the two password fields match."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])

        return password2

    def save(self, commit=True):
        """Save the player, creating or updating the user if necessary."""
        player = super(RegisterForm, self).save(commit=False)

        def grab(s):
            return self.cleaned_data.get(s)

        email = grab('email')
        password = grab('password1')

        try:
            user = User.objects.get(email=email)
            user.set_password(password)

        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                username=email,
                password=password,
            )

        finally:
            user.first_name = grab("first_name")
            user.last_name = grab("last_name")
            user.full_clean()
            user.save()

        player.user = user
        player.game = Game.imminent_game()

        if commit == True:
            player.save()

        return player
