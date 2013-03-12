from django.db import models
from markupfield import fields


class BaseRule(models.Model):
    class Meta:
        abstract = True
        ordering = ('position',)

    title = models.CharField(max_length=100)
    body = fields.MarkupField(default_markup_type='markdown')
    position = models.PositiveIntegerField(default=0)


    def __unicode__(self):
        return u"{}".format(self.title)


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
