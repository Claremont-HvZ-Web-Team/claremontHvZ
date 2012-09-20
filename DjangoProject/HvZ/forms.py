from django import forms

from models import Building, School

import datetime
from math import floor


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

    t = datetime.now()
    cur_hour = t.hour % 12
    cur_min = t.minute - t.minute % 5
    cur_ap = int(floor(t.hour / 12))
    if cur_hour == 0:
        cur_hour = 12
        cur_ap = (cur_ap + 1) % 2

    feed_code = forms.CharField(label='Feed Code',
        max_length=5, min_length=5,
        help_text="<div class='reminder'>Type in the 5 letter feed code of the person you ate</div>",
    )
    meal_day = forms.ChoiceField(
        choices=DAYS, initial=t.weekday(), required=True,
        widget=forms.RadioSelect,
        help_text="<div class='reminder'>Select the day that you ate them.</div>",
    )
    meal_hour = forms.ChoiceField(label="Meal Time",
        choices=HOURS, initial=cur_hour, required=True,
    )
    meal_mins = forms.ChoiceField(label=" ",
        choices=MINS, initial=cur_min, required=True)
    meal_ap = forms.ChoiceField(label="",
        choices=AP, initial=cur_ap, required=True,
        help_text="<div class='reminder'>Select the time of the meal; if you can't remember just type in now.</div>",
    )
    location = forms.ModelChoiceField(queryset=Building.objects.all().order_by('name'), required=False, empty_label="Don't Remember",
        help_text="<div class='reminder'>Select the name of the closest building or landmark to the meal</div>",
    )
    description = forms.CharField(label='Description',
        required=False,
        widget=forms.Textarea,
        help_text="<div class='reminder'>If you got a particularly epic meal, go ahead and describe it here</div>",
    )


class RegForm(forms.Form):
    first = forms.CharField(label='First Name',
        required=True,
        max_length=30,
        help_text="<div class='reminder'>Your First Name</div>",
    )
    last = forms.CharField(label='Last Name',
        required=True,
        max_length=30,
        help_text="<div class='reminder'>Your Last Name</div>",
    )
    email = forms.EmailField(label='Email Address',
        required=True,
        help_text="<div class='reminder'>Enter in an email address that you check regularly since you will be receiving game updates approximately 3 times per day during the week of the game. This email address will also be used to log you in to the website</div>",
    )
    password = forms.CharField(required=True,
        widget=forms.PasswordInput,
        help_text="<div class='reminder'>Enter a password that will be easy for you to remember but difficult for others to guess.</div>",
    )
    school = forms.ModelChoiceField(queryset=School.objects.all().order_by('name'),
        required=True,
        empty_label="None",
        help_text="<div class='reminder'>Select which school you attend. If you do not attend one of the 7Cs, select \"None\".</div>",
    )
    dorm = forms.ModelChoiceField(queryset=Building.objects.filter(building_type='D').order_by('name'),
        required=True,
        empty_label="Off Campus",
        help_text="<div class='reminder'>Select which dorm you expect to sleep in on most nights during the game. If you do not live on campus, select \"Off Campus\"</div>",
    )
    grad = forms.ChoiceField(label='Graduation Year', choices=(("2011", "2011"), ("2012", "2012"), ("2013", "2013"), ("2014", "2014"), ("2015", "2015"), ("2016", "2016"), ("2017", "2017"), ("", "Not a Student")), initial="2011", required=False, help_text="<div class='reminder'>Select which year you expect to graduate. If you don't know yet, select 5 years after the fall of your first year.</div>")
    cell = forms.DecimalField(max_digits=10, decimal_places=0, required=False, help_text="<div class='reminder'>If you want to be able to text message the game's website enter in your phone number here. Include the area code, but do not include hyphens or the leading 1. We will not use this number except in emergencies or in response to texts from you.</div>")
    oz = forms.BooleanField(label='OZ Pool',
        required=False,
        help_text="<div class='reminder'>Check this box if you would like to begin afflicted with the zombie curse.</div>",
    )
    c3 = forms.BooleanField(label='C3 Pool',
        required=False,
        help_text="",
    )
    hardcore = forms.BooleanField(label='Legendary Mode',
        required=False,
        help_text="<div class='reminder'>Check this box if you would like to receive emails about Legendary missions. Legendary missions are available for players who want more plot and story in their game and include challenges that involve critical thinking, difficult side quests, and skills that may not arise in a typical game of HvZ.</div>",
    )
    feed = forms.CharField(label='Feed Code',
        min_length=5, max_length=5,
        required=True,
        help_text="<div class='reminder'>When you are finished entering in all of your other information, have the tabler registering you type in your feed code.<br />TABLERS: Feed codes can only contain the letters A, C, E, L, N, O, P, S, T, W, X, and Z.</div>",
    )


class LoginForm(forms.Form):
    email = forms.CharField(label='Email Address',
        required=True,
        help_text="<div class='reminder'>The email address you used to register for the game.</div>",
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        help_text="<div class='reminder'>Your password for our HvZ site.</div>",
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
        help_text="<div class='reminder'>Type the title of the new thread.</div>",
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea,
        help_text="<div class='reminder'>Type the first post in the new thread.</div>",
    )
    visibility = forms.ChoiceField(
        required=True,
        choices=TEAMS,
        help_text="<div class='reminder'>Select who can see and reply to this thread.</div>",
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
        help_text="<div class='reminder'>Type the contents of your reply.</div>",
    )


class ResetForm(forms.Form):
    email = forms.EmailField(label='Email Address',
        required=True,
        help_text="<div class='reminder'>Enter in the email address you used to register for the game. This is the same address that you received a password reset email in.</div>",
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        help_text="<div class='reminder'>Enter a password that will be easy for you to remember but difficult for others to guess.</div>",
    )
    hash = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput,
    )

