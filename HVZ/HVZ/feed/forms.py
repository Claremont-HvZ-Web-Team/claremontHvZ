from django import forms

from HVZ.main.forms import FeedCodeField
from HVZ.main.models import Building, Game
from HVZ.feed.validators import human_with_code
from HVZ.feed.widgets import SelectTimeWidget

import calendar
import datetime

CAL = calendar.TextCalendar(firstweekday=6)


def get_nearest_hour():
    now = datetime.datetime.now()
    return datetime.datetime(
        now.year, now.month, now.day,
        now.hour,
    )


class MealForm(forms.Form):

    feedcode = FeedCodeField(
        label="Feed code",
        help_text="Type in the feed code of the person you ate",
        validators=[human_with_code],
    )

    # given just one week to register feeds, only need to track
    # what day of week they ate.
    day = forms.ChoiceField(
        choices=(
            # only show days that are between start and end of current game
            (i, CAL.formatweekday(i, 3)) for i in CAL.iterweekdays()
            if i <= Game.imminent_game().end_date.weekday()
            and i >= Game.imminent_game().start_date.weekday()
        ),
        initial=datetime.date.today().weekday,
    )

    time = forms.TimeField(
        required=True,
        widget=SelectTimeWidget(
            minute_step=5,
            twelve_hr=True,
        ),
        initial=get_nearest_hour,
    )

    location = forms.ModelChoiceField(
        Building.objects,
        required=False,
    )

    description = forms.CharField(
        widget=forms.Textarea,
        required=False,
    )

    def clean_time(self):
        try:
            super(MealForm, self).clean_time()
        except AttributeError:
            pass

        if (
            self.cleaned_data['time'] > datetime.datetime.now().time() or
            int(self.cleaned_data['day']) > datetime.date.today().weekday()
        ):
            raise forms.ValidationError("You can't eat in the future, bro.")

        return self.cleaned_data['time']

    def clean(self, *args, **kwargs):
        cleaned_data = super(MealForm, self).clean(*args, **kwargs)

        if not 'day' in cleaned_data:
            raise forms.ValidationError("Somehow you didn't specify the day.")

        game_end = Game.imminent_game().end_date
        offset = (game_end.weekday() - int(cleaned_data['day'])) % 7
        feed_date = game_end - datetime.timedelta(days=offset)

        if feed_date < Game.imminent_game().start_date:
            raise forms.ValidationError("Can't have eaten before the game!")
        cleaned_data['day'] = feed_date

        return cleaned_data
