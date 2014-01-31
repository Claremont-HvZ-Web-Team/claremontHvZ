import os

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):

        print("Synchronizing the database...")
        delimit()
        call_command('syncdb', interactive=True)

        delimit()
        print("Synchronized!")

        try:
            print("Loading colleges data...")
            delimit()

            call_command(
                'loaddata',
                os.path.join(
                    settings.PROJECT_PATH,
                    'HVZ', 'main', 'fixtures', 'production.json'
                )
            )

            delimit()
            print("Data loaded!")

        except CommandError:
            print("Data loading failed!")

        print("Compiling style files...")
        delimit()
        try:
            call_command('compilecss')
        except CommandError:
            print("Style compilation failed!")

        print("Collecting static files...")
        delimit()

        try:
            call_command('collectstatic', interactive=False)
        except CommandError:
            delimit()
            print("Static file collection failed!")

        print("Running unit tests...")
        delimit()
        call_command('test', 'HVZ')

        delimit()
        print("Build Complete!")
        delimit()

def delimit():
    print('-' * 79)
