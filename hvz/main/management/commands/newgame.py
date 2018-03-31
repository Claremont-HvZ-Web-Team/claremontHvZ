import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from hvz.main.models import Game

SUNDAY = 6
MONDAY = 0
TUESDAY = 1
SATURDAY = 5

class Command(BaseCommand):

    def handle(self, *args, **options):
        now = settings.NOW()
        start_date = now.date()

        # The game starts or started on a Tuesday of this week
        if start_date.weekday() in (SUNDAY, MONDAY, TUESDAY):
            start_date -= datetime.timedelta((TUESDAY - start_date.weekday()) % 7)
        else:
            start_date += datetime.timedelta((start_date.weekday() - TUESDAY) % 7)

        if Game.objects.filter(start_date=start_date).exists():
            self.stderr.write("You don't need to create a game!")
            return

        game = Game(start_date=start_date)
        game.full_clean()
        game.save()

        self.stderr.write(
            "Game created from {:%A %d}, {:%B %Y}".format(
                start_date,
                start_date,
            )
        )
