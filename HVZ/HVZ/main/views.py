from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from HVZ.feed.models import Meal
from HVZ.main.models import Game, Player
from HVZ.main.forms import RegisterForm
from HVZ.main.decorators import require_unfinished_game


class LandingPage(TemplateView):
    template_name = "main/landing_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(LandingPage, self).get_context_data(*args, **kwargs)

        if not self.request.user.is_authenticated():
            form = AuthenticationForm()
        else:
            form = None

        context['login_form'] = form
        context['is_landing_page'] = True
        context['latest_meals'] = Meal.objects.all().order_by('time')[:20]
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
        def grab(s):
            return form.cleaned_data[s]

        try:
            u = User.objects.get(email=grab("email"))
            u.set_password(grab("password1"))
        except User.DoesNotExist:
            u = User.objects.create_user(
                email=grab("email"),
                username=grab("email"),
                password=grab("password1"),
            )
        finally:
            u.first_name = grab("first_name")
            u.last_name = grab("last_name")
            u.save()

        p = Player(
            user=u,
            game=Game.nearest_game(),
            school=grab("school"),
            dorm=grab("dorm"),
            grad_year=grab("grad_year"),
            cell=grab("cell"),
            feed=grab("feed"),
            can_oz=grab("can_oz"),
            can_c3=grab("can_c3"),
            team="H",
        )
        p.save()

        return super(Register, self).form_valid(form)
