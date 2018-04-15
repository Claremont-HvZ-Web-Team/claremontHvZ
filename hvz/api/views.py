import json

from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.urls import reverse
from django .conf import settings

from hvz.main.models import Player
from hvz.api.forms import MailerForm

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
        return reverse("mail_success")

    def form_valid(self, form):
        sender = "hvzwattest@gmail.com"
        # sender = "mod@claremonthvz.org"
        if form.is_valid():
            # send email using the self.cleaned_data dictionary
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            recipient_title = form.cleaned_data['recipient']

            # based on inputs from the recipients field, retrieve the list of players 
            # to send emails to, options are:
            # all players, humans, or zombies
            if(recipient_title == MailerForm.ALLPLAYERS):
                recipients = [p.user.email for p in Player.current_players()]

            elif(recipient_title == MailerForm.HUMANS):
                recipients = [p.user.email for p in Player.current_players() if p.team == "H"]

            elif(recipient_title == MailerForm.ZOMBIES):
                recipients = [p.user.email for p in Player.current_players() if p.team == "Z"]        
            # Create an EmailMessage objwct with our given parameters
            mailBag = EmailMessage(subject, body, sender, [], recipients)
            # Check if the user uploaded an attachment (POST), and attach 
            # it to all messages if so
            if self.request.method == 'POST':
                if(self.request.FILES):
                    attachment = self.request.FILES['attachment']
                    mailBag.attach(attachment.name, attachment.read(), attachment.content_type)

        # Send the emails out!
        mailBag.send(fail_silently=False)
        
        return super(Mailer, self).form_valid(form)
