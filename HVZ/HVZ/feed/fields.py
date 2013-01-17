from django.core.exceptions import ValidationError
from django.db import models

class FeedCodeField(models.CharField):

    # The length of a feed code.
    FEED_LEN = 6

    # The characters we allow in a feed code.
    VALID_CHARS = ["A", "C", "E", "L", "K", "N", "P", "Q", "S", "T", "W", "Z"]

    def validate_length(feedcode):
        """Raise an exception if our length is not exactly FEED_LEN."""
        if len(feedcode) != FEED_LEN:
            raise ValidationError(
                u"The feedcode must be exactly {} characters.".format(FEED_LEN))

    def validate_letters(feedcode):
        """Raise an exception if we contain unapproved characters."""
        for c in feedcode:
            if c not in VALID_CHARS:
                raise ValidationError(u"{} is not a valid character!".format(c))

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = self.FEED_LEN
        return super(FeedCodeField, self).__init__(*args, **kwargs)

    default_validators = (models.CharField.default_validators +
                          [validate_length, validate_letters])
