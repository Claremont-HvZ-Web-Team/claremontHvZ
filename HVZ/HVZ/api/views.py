import json

from django.http import HttpResponse

from HVZ.main.models import Player
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from HVZ.api.forms import MailerForm


def json_get_all_emails(request):
    """A function that displays all emails.

    You should replace this with one you actually want.

    """

    # Check out HVZ/main/models.py for helper functions relating to Players.
    # Player.current_players() returns all Players in the current Game.
    emails = [p.user.email for p in Player.current_players()]

    # json.dumps creates a string from a Python object. You can then
    # read the string and convert it into an Objective-C data
    # structure using NSJSONSerialization in Objective-C.
    json_data = json.dumps(emails)

    return HttpResponse(
        json_data,
        content_type="application/json"
    )

class Mailer(FormView):
    form_class = MailerForm
    template_name = "api/mailer.html"

    def dispatch(self, *args, **kwargs):
        return super(Mailer, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse("success")

    def form_valid(self, form):
        form.save()
        return super(Mailer, self).form_valid(form)

