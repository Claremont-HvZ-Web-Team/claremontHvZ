from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from HVZ.main.models import Game
from HVZ.feed.models import Meal
from HVZ.main.forms import PrettyAuthForm, RegisterForm
from HVZ.main.decorators import require_unfinished_game


class LandingPage(TemplateView):
    template_name = "main/landing_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(LandingPage, self).get_context_data(*args, **kwargs)

        if not self.request.user.is_authenticated():
            form = PrettyAuthForm()
        else:
            form = None

        context['login_form'] = form
        context['is_landing_page'] = True
        try:
            context['latest_meals'] = (
                Meal.objects.filter(
                    eater__game=Game.games(started=True).latest(),
                ).order_by('-time')[:20])
        except Game.DoesNotExist:
            context['latest_meals'] = [
                {
                    'time': settings.NOW(),
                    'eater': "ZombieJohn{}".format(x),
                    'eaten': "HumanGreg{}".format(x),
                    'location': None if x % 2 else "HOCH",
                } for x in range(15)
            ]
        return context


class Register(FormView):
    form_class = RegisterForm
    template_name = "main/register.html"

    @method_decorator(permission_required("main.add_player"))
    @method_decorator(require_unfinished_game)
    def dispatch(self, *args, **kwargs):
        return super(Register, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse("register")

    def form_valid(self, form):
        form.save()
        return super(Register, self).form_valid(form)
