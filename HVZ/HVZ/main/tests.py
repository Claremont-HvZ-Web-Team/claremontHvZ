from datetime import timedelta

from django.core import management
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import Client
from django.test.utils import override_settings

from HVZ.basetest import BaseTest, define_user
from HVZ.main import models, forms


HUGH_MANN = define_user({
        "first_name": "Hugh",
        "last_name": "Mann",
        "email": "hmann@hmc.edu",
        "password": "hunter2",
        "school": "4",
        "dorm": "208",
        "grad_year": "2013",
        "cell": "1234567890",
        "feed": "PLANS",
})

class SignupTest(BaseTest):

    def test_tabler_required(self):
        """Ensure the registration page requires a logged-in tabler."""
        c = Client()
        url_register = reverse("register")
        url_login = reverse("login")
        response = c.get(url_register, follow=True)
        self.assertRedirects(response, "{}/?next={}".format(url_login, url_register))

    def test_valid_signup(self):
        """Ensure a player can sign up with valid data."""
        registered = User.objects.filter(username=HUGH_MANN["email"]).exists

        self.assertFalse(registered())
        self.assertEqual(models.Player.objects.count(), 0)

        c = Client()
        self.login_as_tabler(c)

        response = c.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

        response = c.post(reverse("register"), HUGH_MANN)
        self.assertRedirects(response, reverse("register"))

        self.assertEqual(models.Player.objects.count(), 1)
        self.assertTrue(registered())

    def test_password_match(self):
        """Ensure that the password fields must match when registering."""
        c = Client()
        self.login_as_tabler(c)

        p = HUGH_MANN.copy()
        p['password2'] = "wrong"

        response = c.post(reverse('register'), p)

        self.assertFormError(
            response, 'form', 'password2',
            forms.RegisterForm.error_messages['password_mismatch']
        )

        self.assertEqual(models.Player.objects.count(), 0)

    def test_double_signup(self):
        """Ensure a Player can't sign up twice for the same Game."""
        c = Client()
        self.login_as_tabler(c)

        self.assertEqual(models.Player.objects.count(), 0)

        c.post(reverse("register"), HUGH_MANN)
        self.assertEqual(models.Player.objects.count(), 1)

        # Try to register again
        response = c.post(reverse("register"), HUGH_MANN)

        self.assertFormError(
            response, "form", "email",
            forms.RegisterForm.error_messages['duplicate_user'],
        )

        self.assertEqual(models.Player.objects.count(), 1)

    def test_invalid_chars(self):
        """Ensure feedcodes with invalid characters throw error messages."""

        d = HUGH_MANN.copy()
        d["feed"] = "XYXYX"

        c = Client()
        self.login_as_tabler(c)
        response = c.post(reverse("register"), d)
        self.assertFormError(response, "form", "feed", "Y is not a valid character.")

    def test_feed_length(self):
        """Ensure a feedcode must have the correct length."""
        d = HUGH_MANN.copy()
        d["feed"] = "PLAN"

        c = Client()
        self.login_as_tabler(c)

        with self.settings(FEED_LEN=5):
            response = c.post(reverse("register"), d)
            self.assertFormError(response, "form", "feed",
                                 "Ensure this value has at least 5 characters (it has 4).")

            d["feed"] = "SPLANS"
            response = c.post(reverse("register"), d)
            self.assertFormError(response, "form", "feed",
                                 "Ensure this value has at most 5 characters (it has 6).")

    def test_duplicate_feeds(self):
        """Ensure that duplicate feed codes aren't allowed."""
        d = HUGH_MANN.copy()
        d["email"] = "newplayer@hmc.edu"

        c = Client()
        self.login_as_tabler(c)

        self.assertEqual(models.Player.objects.count(), 0)
        self.assertEqual(models.User.objects.count(), 1)

        c.post(reverse("register"), HUGH_MANN)

        self.assertEqual(models.Player.objects.count(), 1)
        self.assertEqual(models.User.objects.count(), 2)

        # Register a different player with the same feed code. Some
        # error should be thrown, and the registration should not go
        # through.
        response = c.post(reverse("register"), d)
        self.assertFormError(response, "form", 'feed',
                             forms.RegisterForm.error_messages['duplicate_feed'],
        )
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(models.Player.objects.count(), 1)

    def test_multi_game(self):
        """Ensure we register players for the newest game when multiple are available."""
        today = self._game_start
        t0 = today - timedelta(weeks=24)
        tf = t0 + timedelta(7)
        old_game = models.Game(start_date=t0, end_date=tf)
        old_game.save()

        c = Client()
        self.login_as_tabler(c)

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
        self.login_as_tabler(c)
        c.post(reverse("register"), HUGH_MANN)

        # Move our Game into the past
        g = models.Game.objects.get()
        g.start_date, g.end_date = self.last_semester()
        g.save()

        # Create a new current Game
        self.create_new_game()

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
        u = models.User.objects.get(username=d["email"])
        self.assertEqual(u.first_name, d["first_name"])
        self.assertEqual(u.last_name, d["last_name"])
        self.assertNotEqual(u.password, old_password)

    def test_long_email(self):
        """Ensure someone with a long email address can register and log in."""

        LONG_EMAIL = "thisisareallylongemailaddress@scrippscollege.edu"

        d = HUGH_MANN.copy()
        d['email'] = LONG_EMAIL

        # Check assumptions
        self.assertEqual(models.Player.objects.count(), 0)
        self.assertEqual(User.objects.count(), 1)

        # Test registration
        c = Client()
        self.login_as_tabler(c)
        response = c.post(reverse('register'), d, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Player.objects.count(), 1)
        self.assertEqual(User.objects.count(), 2)

        # Test login
        response = c.post(reverse('login'), d, follow=True)
        self.assertEqual(response.status_code, 200)


class RandomPlayerTest(BaseTest):

    @override_settings(PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',))
    def test_small(self):
        num_players = 12
        num_ozs = 6
        names = "misc/names.pickle"
        password = "fdsa"
        management.call_command(
            "randomplayers",
            players=num_players,
            ozs=num_ozs,
            names=names,
            password=password,
        )
        self.assertEqual(num_players, models.Player.objects.count())
        self.assertEqual(num_ozs, models.Player.objects.filter(team='Z').count())
