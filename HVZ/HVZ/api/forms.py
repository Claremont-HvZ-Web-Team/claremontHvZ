from django import forms
from HVZ.main.models import Player
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
	
	# Initial version is just to add schools to the same dropdown menu
	#
	# Plan is to allow either another dropdown menu (just for schools) in addition to
	# this one or allow for multiple options to be checked off or something similar
	KindCHOICES = [
		(ALLPLAYERS, "All Players"),
		(HUMANS, "Humans"),
		(ZOMBIES, "Zombies")]

	SchoolCHOICES = [
		('Mudd', 'Mudd'),
		('CMC', 'CMC'),
		('Pitzer', 'Pitzer'),
		('Pomona', 'Pomona'),
		('Scripps', 'Scripps')]
	sender = "hvzwattest@gmail.com"
	# sender = "mod@claremonthvz.org"

	#Email Field validates that the given value is a valid email address
	recipient = forms.ChoiceField(
		label=_("To:"),
		required=True, 
		choices = KindCHOICES
		)
	school = forms.MultipleChoiceField(
		choices = SchoolCHOICES,
		widget = forms.CheckboxSelectMultiple(),
		required = False)
	subject = forms.CharField(
		label=_("Subject:"),
		required=False
		)

	body = forms.CharField(
		label=_("Body:"),
		required=True,
		widget=forms.Textarea()
		)

	def send_email(self):
		# send email using the self.cleand_data dictionary
		pass
