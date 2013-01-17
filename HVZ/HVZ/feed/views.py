from django.views.generic.edit import CreateView

from HVZ.main.utils import current_players

from forms import MealForm

class MealCreate(CreateView):
    form_class = MealForm

    @login_required
    def dispatch(self, *args, **kwargs):
        return super(MealFormView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        fc = form.cleaned_data["feedcode"]

        form.instance.eater = logged_in_player(self.request)
        form.instance.eaten = current_players().get(feed=fc)

        return super(MealFormView, self).form_valid(form)
