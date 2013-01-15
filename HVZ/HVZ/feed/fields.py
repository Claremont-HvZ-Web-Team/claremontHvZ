from django.core.exceptions import ValidationError
from django.db import models

def validate_feed(feedcode):
    """Raise an exception if the feed code contains unapproved characters."""
    for c in feedcode:
        if c not in FeedCodeField.VALID_LETTERS:
            raise ValidationError(u'{} is not a valid character!'.format(c))

class FeedCodeField(models.CharField):
    FEED_LEN = 6
    VALID_LETTERS = ["A", "C", "E", "L", "K", "N", "P", "Q", "S", "T", "W", "Z"]

    default_validators = [validate_feed]

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = self.FEED_LEN
        super(FeedCodeField, self).__init__(*args, **kwargs)
