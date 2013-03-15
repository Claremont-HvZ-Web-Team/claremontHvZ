from datetime import timedelta

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.test import TestCase

from HVZ.main import models

def define_user(d):
    """Modify a dictionary d to describe a Django User.

    Mostly by adding redundant fields.

    """
    d["password1"] = d["password2"] = d["password"]
    d["username"] = d["email"]
    return d

class BaseTest(TestCase):
    """Commonly used code and convenience functions for other TestCases."""

    fixtures = ["production.json"]

    @classmethod
    def setUpClass(cls):
        """Create an initial game and tabler."""
        # Create a current Game.
        cls._game_start = settings.NOW().date()
        cls.create_new_game(cls._game_start)

        tabler = auth_models.User.objects.create_user(
            username="tabler",
            password="a",
        )

        ts = auth_models.Group.objects.create(name="Tablers")
        ts.permissions.add(
            auth_models.Permission.objects.filter(codename="add_player").get()
        )
        ts.user_set.add(tabler)
        ts.save()

    @classmethod
    def tearDownClass(cls):
        """Delete all Games and Users."""
        models.Game.objects.all().delete()
        models.User.objects.all().delete()
        auth_models.Group.objects.all().delete()

    @staticmethod
    def login_as_tabler(client):
        """Log the given Client in as a tabler."""
        return client.login(username="tabler", password="a")

    @staticmethod
    def last_semester():
        """Return a pair of values corresponding to a fake previous game."""
        today = settings.NOW().date()
        t0 = today - timedelta(weeks=26)
        tf = t0 + timedelta(7)
        return (t0, tf)

    @staticmethod
    def create_new_game(game_start=None):
        """Create a Game starting today and lasting a week."""
        if game_start is None:
            game_start = settings.NOW().date()

        g = models.Game(
            start_date=game_start,
            end_date=game_start + timedelta(6),
        )
        g.full_clean()
        g.save()
        return g
