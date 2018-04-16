from django.conf import settings
from django.template import Library

register = Library()

@register.simple_tag
def mod_email():
    return settings.MODERATOR_EMAIL
