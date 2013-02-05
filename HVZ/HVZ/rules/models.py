from django.db import models
from markupfield import fields

class BaseRule(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=100)
    body = fields.MarkupField()

class CoreRule(BaseRule):
    """Rules that are fundamental to the game."""
    pass

class LocationRule(BaseRule):
    """Describe the game in different areas."""
    pass

class ClassRule(BaseRule):
    """Describe the behavior of superhumans."""
    pass

class SpecialInfectedRule(BaseRule):
    """Describe the behavior of superzombies."""
    pass
