from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.views.generic.edit import FormView

from HVZ.main.models import Player
from HVZ.main.forms import RegisterForm
from HVZ.main.decorators import require_unfinished_game
from HVZ.main.utils import nearest_game

class Register(FormView):
    form_class = RegisterForm
    template_name = "register.html"

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
            u = User.objects.create_user(email=grab("email"),
                                         username=grab("email"),
                                         password=grab("password1"))
        finally:
            u.first_name=grab("first_name")
            u.last_name=grab("last_name")
            u.full_clean()
            u.save()

        p = Player(user=u,
                   game=nearest_game(),
                   school=grab("school"),
                   dorm=grab("dorm"),
                   grad_year=grab("grad_year"),
                   cell=grab("cell"),
                   feed=grab("feed"),
                   can_oz=grab("can_oz"),
                   can_c3=grab("can_c3"),
                   team="H")
        p.full_clean()
        p.save()

        return super(Register, self).form_valid(form)
