from django.db.models.signals import post_syncdb
from django.conf import settings

import pybb.models

def create_forums(sender, **kwargs):
    """Create hardcoded pybb forums."""
    for category_name in settings.CATEGORIES:
        c, created = pybb.models.Category.objects.get_or_create(name=category_name)
        if created:
            print('Created category "{}"'.format(c.name))

        for forum_name in settings.FORUMS:
            pybb.models.Forum.objects.get_or_create(category=c, name=forum_name)

post_syncdb.connect(create_forums, sender=pybb.models)
