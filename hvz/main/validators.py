from django.conf import settings
from django.core.exceptions import ValidationError

def validate_feedcode_chars(feedcode):
    """OLD: Raise an exception if we contain unapproved characters.
    NEW: All feedcode characters are valid"""
    # for c in feedcode:
    #     if c not in settings.VALID_CHARS:
    #         raise ValidationError(u"{} is not a valid character.".format(c))
    return
