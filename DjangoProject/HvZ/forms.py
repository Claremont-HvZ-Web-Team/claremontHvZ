from django import forms
from django.contrib.auth.models import User
from django.contrib.localflavor.us.forms import USPhoneNumberField

from models import Building, School

import datetime
from math import floor

def oldest_class_year():
    """Return the year of the oldest class in school right now."""
    return datetime.datetime.now().year

def youngest_class_year():
    """Return the year of the youngest class in school right now."""
    return datetime.datetime.now().year + 4

class EatForm(forms.Form):
    DAYS = (
        ("0", "Monday"),
        ("1", "Tuesday"),
        ("2", "Wednesday"),
        ("3", "Thursday"),
        ("4", "Friday"),
        ("5", "Saturday"),
        ("6", "Sunday"),
    )

    HOURS = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
    )

    MINS = (
        ("00", "00"),
        ("05", "05"),
        ("10", "10"),
        ("15", "15"),
        ("20", "20"),
        ("25", "25"),
        ("30", "30"),
        ("35", "35"),
        ("40", "40"),
        ("45", "45"),
        ("50", "50"),
        ("55", "55"),
    )

    AP = (
        ("0", "AM"),
        ("1", "PM"),
    )

    t = datetime.datetime.now()
    cur_hour = t.hour % 12
    cur_min = t.minute - t.minute % 5
    cur_ap = int(floor(t.hour / 12))
    if cur_hour == 0:
        cur_hour = 12
        cur_ap = (cur_ap + 1) % 2

    feed_code = forms.CharField(label='Feed Code',
        max_length=5, min_length=5,
        help_text="Type in the 5 letter feed code of the person you ate",
    )
    meal_day = forms.ChoiceField(
        choices=DAYS, initial=t.weekday(), required=True,
        widget=forms.RadioSelect,
        help_text="Select the day that you ate them.",
    )
    meal_hour = forms.ChoiceField(label="Meal Time",
        choices=HOURS, initial=cur_hour, required=True,
    )
    meal_mins = forms.ChoiceField(label=" ",
        choices=MINS, initial=cur_min, required=True)
    meal_ap = forms.ChoiceField(label="",
        choices=AP, initial=cur_ap, required=True,
        help_text="Select the time of the meal; if you can't remember just type in now.",
    )
    location = forms.ModelChoiceField(queryset=Building.objects.filter(building_type='D').order_by('name'), required=False, empty_label="Don't Remember",
        help_text="Select the name of the closest building or landmark to the meal",
    )
    description = forms.CharField(label='Description',
        required=False,
        widget=forms.Textarea,
        help_text="If you got a particularly epic meal, go ahead and describe it here",
    )

class UserEmailField(forms.EmailField):
    """Checks that no user has its email address."""
    def validate(self, email):
        super(UserEmailField, self).validate(email)
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("An account with that email already exists.")

class FeedCodeField(forms.CharField):
    """Used to hold feed codes.

    Feed Codes are strings consisting of a restricted subset of
    uppercase letters, chosen by the mod team.

    """
    validLetters = ["A", "C", "E", "L", "K", "N", "P", "Q", "S", "T", "W", "Z"]

    def list_valid_letters(self):
        return ', '.join(self.validLetters)

    def validate(self, feedCode):
        feedCode = feedCode.upper()
        for letter in feedCode:
            if letter not in self.validLetters:
                raise forms.ValidationError(letter + " is not a valid feed code letter.")
        return feedCode


class RegForm(forms.Form):
    first = forms.CharField(label='First Name',
        required=True,
        max_length=30,
        help_text="Your first name",
    )
    last = forms.CharField(label='Last Name',
        required=True,
        max_length=30,
        help_text="Your last name",
    )
    email = UserEmailField(label='Email Address',
        required=True,
        help_text="Enter in an email address that you check regularly since you will be receiving game updates approximately 3 times per day during the week of the game. This email address will also be used to log you in to the website",
    )
    password = forms.CharField(required=True,
        widget=forms.PasswordInput,
        help_text="Enter a password that will be easy for you to remember but difficult for others to guess.",
    )
    school = forms.ModelChoiceField(queryset=School.objects.all().order_by('name'),
        required=True,
        empty_label="Select a school",
        help_text="Select which school you attend. If you do not attend one of the 7Cs, select \"None\".",
    )
    dorm = forms.ModelChoiceField(queryset=Building.objects.filter(building_type='D').order_by('name'),
        required=True,
        empty_label="Select a dorm",
        help_text="Select which dorm you expect to sleep in on most nights during the game. If you do not live on campus, select \"Off Campus\"",
    )
    grad = forms.ChoiceField(label='Graduation Year', choices=(("2011", "2011"), ("2012", "2012"), ("2013", "2013"), ("2014", "2014"), ("2015", "2015"), ("2016", "2016"), ("2017", "2017"), ("", "Not a Student")), initial="2011", required=False, help_text="Select which year you expect to graduate. If you don't know yet, select 5 years after the fall of your first year.")
    cell = USPhoneNumberField(required=False, help_text="If you want to be able to text message the game's website enter in your phone number here. We will not use this number except in emergencies or in response to texts from you.")
    oz = forms.BooleanField(label='OZ Pool',
        required=False,
        help_text="Check this box if you would like to begin afflicted with the zombie curse.",
    )
    c3 = forms.BooleanField(label='C3 Pool',
        required=False,
        help_text="Check this box if you would like to begin as a member of C3.",
    )
    hardcore = forms.BooleanField(label='Legendary Mode',
        required=False,
        help_text="Check this box if you would like to receive emails about Legendary missions. Legendary missions are available for players who want more plot and story in their game and include challenges that involve critical thinking, difficult side quests, and skills that may not arise in a typical game of HvZ."
    )
    feed = FeedCodeField(label='Feed Code',
        min_length=5,
        max_length=5,
        required=True,
        help_text="When you are finished entering in all of your other information, have the tabler registering you type in your feed code. TABLERS: Feed codes can only contain the letters {0}.".format(FeedCodeField.list_valid_letters(FeedCodeField()))
    )


class LoginForm(forms.Form):
    email = forms.CharField(label='Email Address',
        required=True,
        help_text="The email address you used to register for the game.",
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        help_text="Your password for our HvZ site.",
    )


class ThreadForm(forms.Form):
    TEAMS = (
        ("B", "Both Teams"),
        ("M", "My Team"),
    )
    #form to create a new forum thread
    #title, description, visibility need to be filled in
    #game, creator, create_time are auto populated
    title = forms.CharField(
        required=True,
        max_length=30,
        help_text="Type the title of the new thread.",
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea,
        help_text="Type the first post in the new thread.",
    )
    visibility = forms.ChoiceField(
        required=True,
        choices=TEAMS,
        help_text="Select who can see and reply to this thread.",
    )


class PostForm(forms.Form):
    #form to create a new forum post
    #contents needs to be filled in
    #parent, creator, create_time are auto populated
    parent = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput,
    )
    contents = forms.CharField(
        required=True,
        widget=forms.Textarea,
        help_text="Type the contents of your reply.",
    )


class ResetForm(forms.Form):
    email = forms.EmailField(label='Email Address',
        required=True,
        help_text="Enter in the email address you used to register for the game. This is the same address that you received a password reset email in.",
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        help_text="Enter a password that will be easy for you to remember but difficult for others to guess.",
    )
    hash = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput,
    )

