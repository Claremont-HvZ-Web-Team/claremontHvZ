from django.db import models
from django.core.exceptions import ValidationError

class FeedCodeField(models.CharField):

    # The length of a feed code.
    FEED_LEN = 6

    # The characters we allow in a feed code.
    VALID_CHARS = ["A", "C", "E", "L", "K", "N", "P", "Q", "S", "T", "W", "Z"]

    def validate_letters(self):
        """Raise an exception if we contain unapproved characters."""
        for c in self:
            if c not in VALID_CHARS:
                raise ValidationError(u"{} is not a valid character!".format(c))

    def __init__(self, *args, **kwargs):
        kwargs["min_length"] = self.FEED_LEN
        kwargs["max_length"] = self.FEED_LEN
        super(FeedCodeField, self).__init__(*args, **kwargs)

    default_validators = (models.CharField.default_validators +
                          [validate_letters])
