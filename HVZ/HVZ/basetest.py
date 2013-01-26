from datetime import date, timedelta

from django.contrib.auth.models import User, Group
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

    @classmethod
    def setUpClass(cls):
        """Create an initial game and tabler."""
        # Create a current Game.
        cls.new_game()

        tabler = User.objects.create_user(username="tabler", password="a")
        tabler.save()

        ts = Group.objects.get(name="Tablers")
        ts.user_set.add(tabler)
        ts.save()

    @classmethod
    def tearDownClass(cls):
        """Delete all Games and Users."""
        models.Game.objects.all().delete()
        models.User.objects.all().delete()

    @staticmethod
    def login_as_tabler(client):
        """Log the given Client in as a tabler."""
        return client.login(username="tabler", password="a")

    @staticmethod
    def last_semester():
        """Return a pair of values corresponding to a fake previous game."""
        today = date.today()
        t0 = today - timedelta(weeks=26)
        tf = t0 + timedelta(7)
        return (t0, tf)

    @staticmethod
    def new_game():
        """Create a Game starting today and lasting a week."""
        today = date.today()
        g = models.Game(start_date=today,
                        end_date=today+timedelta(7))
        g.save()
        return g
