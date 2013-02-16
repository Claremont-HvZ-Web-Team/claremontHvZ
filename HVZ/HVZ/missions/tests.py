"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import datetime

from django.core.urlresolvers import reverse
from django.test.client import Client

from HVZ.basetest import BaseTest, define_user
from HVZ.main.models import Player, Game
from HVZ.missions.models import Mission, Plot

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
        "feed": "PLANS",
})

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

MISSION = Mission(
    day=datetime.today(),
    time="N",
)

ZOMBIE_PLOT = Plot(
    title="Tonight, we dine in Hell!",
    slug="tonight-we-dine-in-hell",

    team='Z',

    before_story="Nommin' in Nam.",
    before_story_markup_type="markdown",

    victory_story="Zombies done won.",
    victory_story_markup_type="markdown",

    defeat_story="Zombies done lost.",
    defeat_story_markup_type="markdown",
)

HUMAN_PLOT = Plot(
    title="Friends, Romans, Countrymen.",
    slug="friends-romans-countrymen",

    team='H',

    before_story="Lend me your ears",
    before_story_markup_type="markdown",

    victory_story="Humans done won.",
    victory_story_markup_type="markdown",

    defeat_story="Humans done lost.",
    defeat_story_markup_type="markdown",
)

class SingleMissionTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        super(SingleMissionTest, cls).setUpClass()

        # Create the mission and its plot views
        MISSION.game = Game.objects.get()
        MISSION.save()

        m = Mission.objects.get()

        HUMAN_PLOT.mission = m
        HUMAN_PLOT.save()

        ZOMBIE_PLOT.mission = m
        ZOMBIE_PLOT.save()

    @classmethod
    def tearDownClass(cls):
        super(SingleMissionTest, cls).tearDownClass()
        Mission.objects.all().delete()
        Plot.objects.all().delete()

    def setUp(self):
        """Create the players who will view the missions."""
        c = Client()
        self.login_as_tabler(c)

        c.post(reverse('register'), ROB_ZOMBIE)
        z = Player.objects.get()
        z.team = 'Z'
        z.save()

        c.post(reverse('register'), HUGH_MANN)

    def test_list_perspectives(self):
        """Check that each team sees a different list of missions."""
        c = Client()

        # Human
        c.post(reverse('login'), HUGH_MANN)
        response = c.get(reverse('plot_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['plot_list'][0], HUMAN_PLOT)

        response = c.post(reverse('login'), ROB_ZOMBIE)
        response = c.get(reverse('plot_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['plot_list'][0], ZOMBIE_PLOT)
