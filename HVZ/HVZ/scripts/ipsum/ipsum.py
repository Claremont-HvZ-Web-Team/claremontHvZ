import random
import itertools

from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth.models import User

from HVZ.main.models import Player, Game, School, Building

NAMES = "names.txt"
PASS = "asdf"
SCHOOLS = School.objects.all()
DORMS = Building.dorms()
FEEDS = itertools.permutations(settings.VALID_CHARS, r=settings.FEED_LEN)

NUM_OZS = 7


def make_players():

    with open(NAMES) as f:
        names = f.readlines()

    game = Game.imminent_game()

    for name in names:
        firstname, lastname = name.split()

        uname = '{}{}@hmc.edu'.format(firstname[0].lower(), lastname.lower())

        try:
            u = User.objects.create_user(username=uname,
                                         password=PASS)
        except IntegrityError:
            continue

        p = Player(user=u,
                   cell="1234567890",
                   game=game,
                   school=random.choice(SCHOOLS),
                   dorm=random.choice(DORMS),
                   grad_year=random.choice(range(2013,2017)),
                   can_oz=(random.random()>0.5),
                   can_c3=(random.random()>0.5),
                   feed=FEEDS.next(),
        )
        p.save()


def pick_ozs():
    oz_ids = random.sample(xrange(1, Player.objects.filter(can_oz=True).count()), NUM_OZS)
    ozs = Player.objects.filter(id__in=oz_ids)
    for p in ozs:
        p.team = 'Z'
        p.upgrade = 'O'
        p.save()


if __name__ == "__main__":
    make_players()
    pick_ozs()
