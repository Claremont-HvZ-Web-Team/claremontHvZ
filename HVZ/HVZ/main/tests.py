"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import date, timedelta

from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

import models

HUGH_MANN = {
    "first_name": "Hugh",
    "last_name": "Mann",
    "email": "hmann@hmc.edu",
    "password1": "hunter2",
    "password2": "hunter2",
    "school": "4",
    "dorm": "208",
    "grad_year": "2013",
    "cell": "1234567890",
    "can_c3": "on",
    "feed": "PLANS"
}

class SignupTest(TestCase):
    def setUp(self):
        # Create a current Game.
        today = date.today()
        g = models.Game(start_date=today,
                        end_date=today+timedelta(7))
        g.save()

        tabler = User.objects.create_user(username="tabler", password="a")
        tabler.save()

        ts = Group.objects.get(name="Tablers")
        ts.user_set.add(tabler)
        ts.save()

    def test_admin_required(self):
        """Ensure the registration page requires a logged-in tabler."""
        c = Client()
        response = c.get(reverse("register"), follow=True)
        self.assertRedirects(response, "/login/?next=%2Fregister%2F")

    def test_valid_signup(self):
        """Ensure a player can sign up with valid data.
        """
        registered = User.objects.filter(username=HUGH_MANN["email"]).exists
        self.assertFalse(registered())

        c = Client()
        c.post(reverse("login"), {"username": "tabler", "password": "a"})

        response = c.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

        response = c.post(reverse("register"), HUGH_MANN)
        self.assertRedirects(response, reverse("register"))

        self.assertTrue(registered())

    def test_double_signup(self):
        """Ensure a Player can't sign up twice for the same Game."""
        c = Client()
        c.post(reverse("login"), {"username": "tabler", "password": "a"})
        c.post(reverse("register"), HUGH_MANN)
        response = c.post(reverse("register"), HUGH_MANN)
        self.assertFormError(response, "form", "email",
                             "{} has already registered for this Game.".format("hmann@hmc.edu"))
