from datetime import date, timedelta

from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.test.client import Client

from HVZ.basetest import BaseTest, define_user
from HVZ.main import models

HUGH_MANN = define_user({
        "first_name": "Hugh",
        "last_name": "Mann",
        "email": "hmann@hmc.edu",
        "password": "hunter2",
        "school": "4",
        "dorm": "208",
        "grad_year": "2013",
        "cell": "1234567890",
        "can_c3": "on",
        "feed": "PLANS"
        })

class SignupTest(BaseTest):
    def login_table(self, c):
        """Convenience function to login as a tabler."""
        return c.post(reverse("login"), {"username": "tabler", "password": "a"})


    def test_tabler_required(self):
        """Ensure the registration page requires a logged-in tabler."""
        c = Client()
        response = c.get(reverse("register"), follow=True)
        self.assertRedirects(response, "/login/?next=%2Fregister%2F")

    def test_valid_signup(self):
        """Ensure a player can sign up with valid data."""
        registered = User.objects.filter(username=HUGH_MANN["email"]).exists
        self.assertFalse(registered())

        c = Client()
        self.login_table(c)

        response = c.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

        response = c.post(reverse("register"), HUGH_MANN)
        self.assertRedirects(response, reverse("register"))

        self.assertTrue(registered())

    def test_double_signup(self):
        """Ensure a Player can't sign up twice for the same Game."""
        c = Client()
        self.login_table(c)
        c.post(reverse("register"), HUGH_MANN)
        response = c.post(reverse("register"), HUGH_MANN)
        self.assertFormError(response, "form", "email",
                             "{} has already registered for this Game.".format(HUGH_MANN["email"]))

    def test_invalid_chars(self):
        """Ensure feedcodes with invalid characters throw error messages."""

        d = HUGH_MANN.copy()
        d["feed"] = "XKXKX"

        c = Client()
        self.login_table(c)
        response = c.post(reverse("register"), d)
        self.assertFormError(response, "form", "feed", "X is not a valid character.")

    def test_feed_length(self):
        """Ensure a feedcode must have the correct length."""
        d = HUGH_MANN.copy()
        d["feed"] = "PLAN"

        c = Client()
        self.login_table(c)

        with self.settings(FEED_LEN=5):
            response = c.post(reverse("register"), d)
            self.assertFormError(response, "form", "feed",
                                 "Ensure this value has at least 5 characters (it has 4).")

            d["feed"] = "SPLANS"
            response = c.post(reverse("register"), d)
            self.assertFormError(response, "form", "feed",
                                 "Ensure this value has at most 5 characters (it has 6).")

    def test_multi_game(self):
        """Ensure we register players for the newest game when multiple are available."""
        today = date.today()
        t0 = today - timedelta(weeks=24)
        tf = t0 + timedelta(7)
        old_game = models.Game(start_date=t0, end_date=tf)
        old_game.save()
        
        c = Client()
        self.login_table(c)

        self.assertFalse(models.Player.objects.filter(game=old_game).exists())
        self.assertFalse(models.Player.objects.filter(game__start_date=today).exists())

        c.post(reverse("register"), HUGH_MANN)
        
        self.assertFalse(models.Player.objects.filter(game=old_game).exists())
        self.assertTrue(models.Player.objects.filter(game__start_date=today).exists())

    def test_user_update(self):
        """Ensure that a user can register once for each game.

        The user's name and password should update with the new info.

        """

        # Register our user
        c = Client()
        self.login_table(c)
        response = c.post(reverse("register"), HUGH_MANN)

        # Move our Game into the past
        g = models.Game.objects.get()
        g.start_date, g.end_date = self.last_semester()
        g.save()

        # Create a new current Game
        self.new_game()

        # Modify our user settings slightly
        d = HUGH_MANN.copy()
        d["first_name"] = "Harold"
        d["last_name"] = "Zoid"
        d["password1"] = "swordfish"
        d["password2"] = "swordfish"

        # Save the old password
        u = models.User.objects.filter(username=d["email"]).get()
        old_password = u.password

        # And register with the new settings
        c.post(reverse("register"), d)

        # There should be two Players and two Users (remember our tabler user)
        self.assertEqual(models.Player.objects.count(), 2)
        self.assertEqual(models.User.objects.count(), 2)

        # And the new User's fields should be those defined by the newest
        # registration.
        u = models.User.objects.filter(username=d["email"]).get()
        self.assertEqual(u.first_name, d["first_name"])
        self.assertEqual(u.last_name, d["last_name"])
        self.assertNotEqual(u.password, old_password)
