from django.db import models

# Create your models here.


class Rule(models.Model):
    CATEGORIES = {
        "L": "Location",
        "C": "Class",
        "B": "Basic",
    }

    category = models.CharField(
        max_length=1,
        choices=[(x, CATEGORIES[x]) for x in CATEGORIES],
    )
