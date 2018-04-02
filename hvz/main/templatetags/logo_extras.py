from django.conf import settings
from django.template import Library

register = Library()

@register.simple_tag
def mission_link():
    return settings.MISSION_DOC_LINK

@register.simple_tag
def rules_link():
    return settings.RULES_DOC_LINK
