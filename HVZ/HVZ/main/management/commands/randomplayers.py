import cPickle
import itertools
import random
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth.models import User

from HVZ.main.models import Player, Game, School, Building


NAMES = "misc/names.pickle"
PASSWORD = "asdf"
SCHOOLS = School.objects.all()
DORMS = Building.dorms()
FEEDS = itertools.permutations(settings.VALID_CHARS, r=settings.FEED_LEN)

NUM_OZS = 7


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-p',
            '--players',
            type='int',
        ),
        make_option(
            '--ozs',
            type='int',
        ),
        make_option(
            '--names',
            type='string',
        ),
        make_option(
            '--password',
            type='string',
        ),
    )

    def handle(self, *args, **options):

        num_players = options.get('players')
        names_file = options.get('names') or NAMES
        num_ozs = options.get('ozs') or NUM_OZS

        self.password = options.get('password') or PASSWORD

        with open(names_file) as f:
            names = cPickle.load(f)

        self.game = Game.imminent_game()
        self.year = settings.NOW().year

        players = list(self.make_players(names[:num_players]))
        Player.objects.bulk_create(players)

        self.pick_ozs(num_ozs)

    def make_players(self, names):
        for firstname, lastname in names:
            uname = '{}{}@hmc.edu'.format(firstname[0].lower(),
                                          lastname.lower())

            try:
                u = User.objects.create_user(username=uname,
                                             password=self.password)
            except IntegrityError:
                continue
            u.first_name = firstname
            u.last_name = lastname
            u.save()

            yield Player(
                user=u,
                cell="1234567890",
                game=self.game,
                school=random.choice(SCHOOLS),
                dorm=random.choice(DORMS),
                grad_year=self.year+random.randint(0, 4),
                can_oz=random.random()>0.5,
                can_c3=random.random()>0.5,
                feed=FEEDS.next(),
            )

    def pick_ozs(self, num_ozs):
        num_candidates = Player.objects.count()
        oz_ids = random.sample(
            xrange(1, num_candidates),
            min(num_ozs, num_candidates),
        )
        ozs = Player.objects.filter(id__in=oz_ids)
        for p in ozs:
            # Retroactively volunteer the mock player
            p.can_oz = True

            p.team = 'Z'
            p.upgrade = 'O'
            p.save()
