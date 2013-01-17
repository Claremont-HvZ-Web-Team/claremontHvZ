from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from models import Player
from forms import SignupForm, RegisterForm

class Signup(CreateView):
    model = User
    form_class = SignupForm
    template_name = "signup.html"
    success_url = "/"

class Register(CreateView):
    model = Player
    form_class = RegisterForm

    @method_decorator(login_required)
    def dispatch(self):
        return super(MealFormView, self).dispatch(*args, **kwargs)
