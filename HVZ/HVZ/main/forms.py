from django import forms

from HVZ.feed.fields import FeedCodeField


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
the letters {}.""".format(FeedCodeField.VALID_LETTERS))

C3_TEXT = """\
Check this box if you would like to begin as a member of C3."""


class UserCreate(forms.ModelForm):
    class Meta:
        model = User

class PlayerCreate(forms.ModelForm):
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
        required=True,
        empty_label="Select a school",
    )

    dorm = forms.ModelChoiceField(
        required=True,
        empty_label="Select a dorm",
    )

    grad_year = forms.PositiveIntegerField(required=True)

    cell = USPhoneNumberField(
        label="Cell Number"
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


