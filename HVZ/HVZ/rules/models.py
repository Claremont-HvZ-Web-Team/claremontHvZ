from django.db import models
from markupfield import fields as markup

class BaseRule(models.Model):
    title = models.CharField(max_length=100)
    body = markup.MarkupField()

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


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
