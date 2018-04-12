# file for code review
import json

from django.http import HttpResponse

from hvz.main.models import Player
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from hvz.api.forms import MailerForm
from django.shortcuts import render
from hvz.api import views
from django.urls import reverse

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

def success(request):
    return render(request, 'api/success.html', {})

class Mailer(FormView):
    form_class = MailerForm
    template_name = "api/mailer.html"

    # return url
    success_url = '/success/'

    def dispatch(self, *args, **kwargs):
        # used to display the form
        return super(Mailer, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        # after the mail is sent successfully, it goes to the success page
        # At this point, it is the same as registration success page
        # in the future, we will have more details 
        
        return reverse("mail_success")

    def form_valid(self, form):

        sender = "hvzwattest4@gmail.com"
        # sender = "mod@claremonthvz.org"
        if form.is_valid():
            # send email using the self.cleand_data dictionary
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            recipient_title = form.cleaned_data['recipient']
        # based on inputs from the recipients field, retrieve the list of players 
        # to send emails to, options are:
        # all players, humans, or zombies

        if(recipient_title == list(MailerForm.ALLPLAYERS)):
            recipients = [p.user.email for p in Player.current_players()]
        elif(MailerForm.HUMANS in recipient_title):
            recipients = [p.user.email for p in Player.current_players() if p.team == "H"]

        elif(MailerForm.ZOMBIES in recipient_title):
            recipients = [p.user.email for p in Player.current_players() if p.team == "Z"]        
        # TODO: Authentication error for sender for mod@claremonthvz.org
        mailBag = EmailMessage(subject, body, sender, [], recipients)
        mailBag.send(fail_silently=False)

        
        return super(Mailer, self).form_valid(form)
