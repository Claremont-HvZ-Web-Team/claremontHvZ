import os
import subprocess

from django.core.management.base import BaseCommand
from django.conf import settings

def get_apps():
    """Return the name of each HVZ subapp."""
    return [x[4:] for x in settings.INSTALLED_APPS if x.startswith('HVZ.')]

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.old_dir = os.getcwd()

        try:
            for app in get_apps():
                static_dir = os.path.join(settings.PROJECT_PATH, 'HVZ', app, 'static')

                if not os.path.exists(static_dir):
                    continue

                if not os.path.exists(os.path.join(static_dir, 'sass')):
                    continue

                self.stdout.write("Compiling {}".format(app))
                os.chdir(os.path.join(settings.PROJECT_PATH, 'HVZ', app, 'static'))
                if not os.path.exists('styles'):
                    os.mkdir('styles')
                subprocess.call(['compass', 'compile',
                                 '--sass-dir', 'sass',
                                 '--css-dir', 'styles'])
        except OSError:
            self.stderr.write("Unable to access the '{}' subapp.".format(app))
        except CalledProcessError as e:
            self.stderr.write("Error writing css in the '{}' subapp\n".format(app))
        finally:
            os.chdir(self.old_dir)
            return
