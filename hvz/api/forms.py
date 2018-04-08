from django import forms
from hvz.main.models import Player
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
#from django_localflavor_us.forms import USPhoneNumberField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

class MailerForm(forms.Form):

	ALLPLAYERS = "All"
	HUMANS = "Humans"
	ZOMBIES = "Zombies"
	CHOICES = [
		(ALLPLAYERS, "All Players"),
		(HUMANS, "Humans"),
		(ZOMBIES, "Zombies"),
	]
	# TODO: Should we make this a field in the email "form?"
	
	sender = "hvzwattest@gmail.com"
	# sender = "mod@claremonthvz.org"

	#Email Field validates that the given value is a valid email address
	recipient = forms.ChoiceField(
		label=_("To:"),
		required=True, 
		choices = CHOICES
		)

	subject = forms.CharField(
		label=_("Subject:"),
		required=True
		)

	body = forms.CharField(
		label=_("Body:"),
		required=True,
		widget=forms.Textarea()
		)

	def send_email(self):
		# send email using the self.cleand_data dictionary
		pass