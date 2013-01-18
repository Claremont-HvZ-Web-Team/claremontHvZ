from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from HVZ.main.decorators import zombie_required
from HVZ.main.utils import current_players

from models import Meal
from forms import MealForm

class MealCreate(CreateView):
    model = Meal
    form_class = MealForm

    @method_decorator(login_required)
    @method_decorator(zombie_required)
    def dispatch(self, *args, **kwargs):
        return super(MealFormView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        fc = form.cleaned_data["feedcode"]

        form.instance.eater = logged_in_player(self.request)
        form.instance.eaten = current_players().get(feed=fc)

        return super(MealFormView, self).form_valid(form)
