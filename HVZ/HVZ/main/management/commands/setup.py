import os
import subprocess

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        old_dir = os.getcwd()

        try:
            print("Copying template files...")
            delimit()

            files = 0

            os.chdir(os.path.join(settings.PROJECT_PATH, 'HVZ'))
            if not os.path.exists('local_settings.py'):
                print("local_settings.py...")
                subprocess.call([
                    'cp',
                    'sample_local_settings.py',
                    'local_settings.py',
                ])
                files += 1

            os.chdir(os.path.join(settings.PROJECT_PATH))
            if not os.path.exists('passenger_wsgi.py'):
                print("passenger_wsgi.py...")
                subprocess.call([
                    'cp',
                    'sample_passenger_wsgi.py',
                    'passenger_wsgi.py',
                ])
                files += 1

            if files > 0:
                delimit()
            print("%d files copied!" % files)

        finally:
            os.chdir(old_dir)

        print("Synchronizing the database...")
        delimit()
        call_command('syncdb', interactive=True)

        print("Compiling CSS files...")
        delimit()
        call_command('compilecss')

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
