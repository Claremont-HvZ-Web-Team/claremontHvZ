import random
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User

from HVZ.main.models import Player, Game, Building
from HVZ.feed.models import Meal


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-m',
            '--meals',
            type='int',
        ),
    )

    def handle(self, *args, **options):
        try:
            self.game = Game.imminent_game()
        except Game.DoesNotExist:
            self.stderr.write("No currently-running game found. Create a game at /admin/ first.")
            return

        humans = Player.current_players().filter(team='H')
        if not len(humans):
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
        Meal.objects.bulk_create(meals)

    def make_meals(self, num_meals):
        humans = list(Player.current_players().filter(team='H'))
        zombies = list(Player.current_players().filter(team='Z'))
        
        g = Game.imminent_game()

        t = g.start_date
        dt = (g.end_date - g.start_date) / num_meals

        for i in xrange(num_meals):
            z = int(random.random() * len(zombies))
            h = int(random.random() * len(humans))

            Meal(
                eater=zombies[z],
                eaten=humans[h],
                time=t,
                location=random.choice(Building.objects.all()),
            ).save()

            t += dt

            # Instead of retrieving the entire zombie and human lists
            # again, why don't we just add the human to the zombie
            # horde ourselves?
            zombies.append(humans.pop(h))
