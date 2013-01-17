from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from forms import SignupForm

class Signup(CreateView):
    model = User
    form = SignupForm
    template_name = "signup.html"
