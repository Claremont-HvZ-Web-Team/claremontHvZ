from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from HVZ.main.decorators import team_required

from models import Meal, Player
from forms import MealForm


class EatView(FormView):
    form_class = MealForm
    template_name = "feed/eat.html"

    @method_decorator(login_required)
    @method_decorator(team_required('Z'))
    def dispatch(self, *args, **kwargs):
        return super(EatView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse("main_landing")

    def form_valid(self, form):
        def grab(s):
            return form.cleaned_data[s]

        m = Meal(
            eater=Player.logged_in_player(self.request),
            eaten=Player.current_players().filter(feed=grab("feedcode")).get(),
            time=grab('time'),
            location=grab("location"),
            description=grab("description"),
        )
        m.full_clean()
        m.save()

        return super(EatView, self).form_valid(form)
