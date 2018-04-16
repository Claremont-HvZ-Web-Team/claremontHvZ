import os
import itertools
import math
import random
import string

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.core.management import call_command
from django.core.management.base import BaseCommand

from hvz.main import models


PASSWORD = "asdf"
FEEDS = itertools.permutations(settings.VALID_CHARS, r=settings.FEED_LEN)

NUM_PLAYERS = 200
NUM_OZS = 7


def random_name():

    firstname = "".join(
        [random.choice(string.ascii_uppercase)] +
        [random.choice(string.ascii_lowercase) for x in range(6)],
    )

    lastname = "".join(
        [random.choice(string.ascii_uppercase)] +
        [random.choice(string.ascii_lowercase) for x in range(8)],
    )
    return firstname, lastname


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--players',
            type=int,
        )
        parser.add_argument(
            '-z',
            '--ozs',
            type=int,
        )
        parser.add_argument(
            '--password',
            type=str,
        )

    def handle(self, *args, **options):

        try:
            self.game = models.Game.nearest_game()
        except models.Game.DoesNotExist:
            self.stderr.write("No currently-running game found.")
            Game.objects.create(start_date=settings.NOW())
            self.game = models.Game.nearest_game()

        self.schools = list(models.School.objects.all())
        self.dorms = list(models.Building.dorms())

        if len(self.schools) == 0 or len(self.dorms) == 0:
            call_command(
                'loaddata',
                os.path.join('hvz', 'main', 'fixtures', 'campus.json'),
                stdout=self.stdout,
                stderr=self.stderr,
            )
            self.schools = list(School.objects.all())
            self.dorms = list(Building.dorms().all())

        num_players = options.get('players') or NUM_PLAYERS
        num_ozs = options.get('ozs') or NUM_OZS

        self.password = options.get('password') or PASSWORD

        self.year = settings.NOW().year

        players = self.make_players(num_players)
        models.Player.objects.bulk_create(players)

        self.pick_ozs(num_ozs)

    def make_players(self, num_players):
        used_feeds = set([p.feed for p in models.Player.current_players()])
        if len(used_feeds) == math.factorial(settings.FEED_LEN):
            return

        for i in range(num_players):

            firstname, lastname = random_name()
            uname = '{}{}@randomplayer.xyz'.format(firstname[0].lower(), lastname.lower())

            try:
                u = auth_models.User.objects.get(username=uname)

            except auth_models.User.DoesNotExist:
                u = auth_models.User.objects.create_user(username=uname,
                                             password=self.password)
                u.first_name = firstname
                u.last_name = lastname
                u.save()

            feed = ''.join(next(FEEDS))
            while feed in used_feeds:
                feed = ''.join(next(FEEDS))
            yield models.Player(
                user=u,
                game=self.game,
                school=random.choice(self.schools),
                dorm=random.choice(self.dorms),
                grad_year=self.year+random.randint(0, 4),
                can_oz=random.random()>0.5,
                feed=feed,
            )

    def pick_ozs(self, num_ozs):
        ozs = models.Player.current_players().order_by('?')[:num_ozs]
        for p in ozs:
            # Retroactively volunteer the mock player
            p.can_oz = True

            p.team = 'Z'
            p.upgrade = 'O'
            p.save()
