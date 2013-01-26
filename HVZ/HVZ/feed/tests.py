from datetime import datetime

from django.core.urlresolvers import reverse
from django.test.client import Client

from HVZ.basetest import BaseTest, define_user
from HVZ.main.models import Player, Game
from HVZ.feed.models import Meal

ROB_ZOMBIE = define_user({
        "first_name": "Rob",
        "last_name": "Zombie",
        "email": "rzed@cmc.edu",
        "password": "hunter2",
        "school": "4",
        "dorm": "208",
        "grad_year": "2013",
        "cell": "1234567890",
        "can_oz": "on",
        "feed": "SNEAK"
        })

VICTIM = define_user({
        "first_name": "Hapless",
        "last_name": "Victim",
        "email": "hv@hmc.edu",
        "password": "swordfish",
        "school": "4",
        "dorm": "208",
        "grad_year": "2015",
        "cell": "1234567890",
        "feed": "EATEN"
        })

MEAL = {
    "time": datetime.now().strftime("%a %b %d %H:%M"),
    "location": "208",
    "description": "I don't want to live on this planet anymore.",
    "feedcode": VICTIM["feed"]
}

class PermissionTest(BaseTest):
    def setUp(self):
        # Create a game and tabler
        super(PermissionTest, self).setUp()

        c = Client()
        self.login_as_tabler(c)
        c.post(reverse("register"), ROB_ZOMBIE)
        c.post(reverse("register"), VICTIM)

    def test_humans_forbidden(self):
        """Ensure that humans can't access the meal page."""
        c = Client()
        c.post(reverse("login"), ROB_ZOMBIE)
        response = c.get(reverse("eat"))
        self.assertEqual(response.status_code, 403)

    def test_humans_cannot_eat(self):
        """Attempt to bypass the meal page and eat as a human anyway."""
        c = Client()
        c.post(reverse("login"), ROB_ZOMBIE)
        response = c.post(reverse("eat"), MEAL)

        # Ensure we were denied and could not create a meal.
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Meal.objects.count(), 0)

    def test_zombies_allowed(self):
        """Ensure that zombies can access the meal page."""

        # Let Rob be a zombie this time.
        z = Player.objects.filter(user__email=ROB_ZOMBIE["email"]).get()
        z.team = "Z"
        z.save()

        # Should allow
        c = Client()
        c.post(reverse("login"), ROB_ZOMBIE)
        response = c.get(reverse("eat"))
        self.assertEqual(response.status_code, 200)

class EatingTest(BaseTest):
    def setUp(self):
        c = Client()
        self.login_as_tabler(c)

        # Create a zombie
        c.post(reverse("register"), ROB_ZOMBIE)
        z = Player.objects.get()
        z.team = "Z"
        z.save()

        # Create a victim
        c.post(reverse("register"), VICTIM)

    def test_eating(self):
        """Ensure that eating creates Meals and turns humans into zombies."""
        c = Client()
        c.post(reverse("login"), ROB_ZOMBIE)

        self.assertEqual(Meal.objects.count(), 0)
        c.post(reverse("eat"), MEAL)

        # Check that a meal was created
        self.assertEqual(Meal.objects.count(), 1)

        # Check that the victim is now a zombie
        victim = Player.objects.filter(user__email=VICTIM["email"]).get()
        self.assertEqual(victim.team, "Z")

    def test_double_eating(self):
        """Ensure a zombie can't eat the same victim twice."""
        c = Client()
        c.post(reverse("login"), ROB_ZOMBIE)
        
        c.post(reverse("eat"), MEAL)
        response = c.post(reverse("eat"), MEAL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Meal.objects.count(), 1)
        self.assertFormError(response, "form", "feedcode",
                             "{} doesn't correspond to a playing human!"
                             .format(VICTIM["feed"]))

    def test_resurrected_eating(self):
        """A zombie can eat the same victim twice with resurrection."""
        c = Client()
        c.post(reverse("login"), ROB_ZOMBIE)
        
        c.post(reverse("eat"), MEAL)
        c.post(reverse("eat"), MEAL)

        self.assertEqual(Meal.objects.count(), 1)

        get_victim = Player.objects.filter(user__email=VICTIM["email"]).get

        # Resurrect the victim
        p = get_victim()
        p.team = "H"
        p.save()

        c.post(reverse("eat"), MEAL)

        # We should have eaten the victim twice.
        self.assertEqual(Meal.objects.count(), 2)
        self.assertEqual(get_victim().team, "Z")

class MultiGame(BaseTest):

    def setUp(self):

        c = Client()
        self.login_as_tabler(c)

        # Create a victim in the past
        c.post(reverse("register"), VICTIM)
        g = Game.objects.get()
        g.start_date, g.end_date = self.last_semester()
        g.save()

        # And a zombie in the present
        self.new_game()
        c.post(reverse("register"), ROB_ZOMBIE)
        z = Player.objects.filter(user__email=ROB_ZOMBIE["email"]).get()
        z.team = "Z"
        z.save()

    def test_cross_game_eating(self):
        """Ensure one can't eat across games."""
        c = Client()
        c.post(reverse("login"), ROB_ZOMBIE)
        response = c.post(reverse("eat"), MEAL)

        self.assertEqual(Meal.objects.count(), 0)

        victim = Player.objects.filter(user__email=VICTIM["email"]).get()
        self.assertEqual(victim.team, "H")
        self.assertFormError(response, "form", "feedcode",
                             "{} doesn't correspond to a playing human!"
                             .format(VICTIM["feed"]))
