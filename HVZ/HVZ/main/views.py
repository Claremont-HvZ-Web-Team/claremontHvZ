from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

class UserCreate(CreateView):
    class Meta:
        model = User
