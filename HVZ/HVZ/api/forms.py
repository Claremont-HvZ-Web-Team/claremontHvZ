from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
#from django_localflavor_us.forms import USPhoneNumberField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

class MailerForm(forms.Form):

	# TODO: Should we make this a field in the email "form?"
	sender = "mods@claremonthv.org"

	#Email Field validates that the given value is a valid email address
	recipient = forms.EmailField(
		label=_("To:"),
		required=True
		)

	subject = forms.CharField(
		label=_("Subject:"),
		required=False
		)

	body = forms.CharField(
		label=_("Body:"),
		required=True
		)