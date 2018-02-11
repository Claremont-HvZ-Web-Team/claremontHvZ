from datetime import datetime, time, timedelta
import random
from optparse import make_option

from django.core.management import call_command
from django.core.management.base import BaseCommand

from hvz.main import models


class Command(BaseCommand):
    def add_argument(self, parser):
        parser.add_argument(
            '-m',
            '--meals',
            type=int,
        )
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
            # Create game and players
            call_command(
                'randomplayers',
                players=options.get('players'),
                ozs=options.get('ozs'),
                password=options.get('password'),
                stdout=self.stdout,
                stderr=self.stderr,
            )
            self.game = models.Game.nearest_game()

        humans = models.Player.current_players().filter(team='H')
        zombies = models.Player.current_players().filter(team='Z')
        if not len(humans) or not len(zombies):
            self.stderr.write(
                '\n'.join(["There are no players in the current game.",
                           "To generate a batch of random players, run",
                           "    ./manage.py randomplayers"]))
            return

        num_meals = options.get('meals') or len(humans) / 2

        self.stdout.write("Creating {} meals".format(num_meals))

        if not num_meals:
            return

        if len(humans) < num_meals:
            self.stderr.write(
                "There are only {} humans in the current game.".format(len(humans))
            )
            num_meals = len(humans)

        meals = self.make_meals(num_meals)
        models.Meal.objects.bulk_create(meals)

    def make_meals(self, num_meals):
        humans = list(models.Player.current_players().filter(team='H'))
        zombies = list(models.Player.current_players().filter(team='Z'))

        g = models.Game.nearest_game()

        day = g.start_date
        days = 7
        while day < g.start_date + timedelta(days=days):

            meals_per_hour = [0 for i in range(24)]
            for i in range(int(num_meals / days)):
                meals_per_hour[int(random.gauss(13, 4)) % 24] += 1

            for hour in range(24):

                for meal in range(meals_per_hour[hour]):
                    z = int(random.random() * len(zombies))
                    h = int(random.random() * len(humans))

                    models.Meal(
                        eater=zombies[z],
                        eaten=humans[h],
                        time=datetime.combine(day, time(hour=hour)),
                        location=random.choice(models.Building.objects.all()),
                    ).save()

                    # Instead of retrieving the entire zombie and human lists
                    # again, why don't we just add the human to the zombie
                    # horde ourselves?
                    zombies.append(humans.pop(h))

            day += timedelta(days=1)
