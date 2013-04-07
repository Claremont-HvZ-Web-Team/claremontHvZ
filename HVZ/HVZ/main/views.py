from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator

from HVZ.main.models import Game, ModSchedule
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
            context['latest_meals'] = []

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


class TwilioCallHandler(TemplateView):
    template_name = "main/call.xml"

    def render_to_response(self, context, **kwargs):
        return super(TwilioCallHandler, self).render_to_response(
            context,
            content_type='text/xml',
            **kwargs
        )

    def get_context_data(self, *args, **kwargs):
        context = super(TwilioCallHandler, self).get_context_data(*args, **kwargs)
        on_duty = ModSchedule.get_current_mod()
        if on_duty:
            context["name"] = on_duty.user.first_name
            context["cell"] = on_duty.cell
        else:
            # this should NOT HAPPEN
            pass

        return context
