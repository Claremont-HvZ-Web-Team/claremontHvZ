import glob
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

        os.chdir(settings.STATIC_ROOT)
        subprocess.call(['compass', 'compile',
                         '--sass-dir', 'sass',
                         '--css-dir', 'styles'])
        
        for app in get_apps():
            try:
                if not os.path.exists(os.path.join('styles', app)):
                    continue

                target_parent_dir = os.path.join(settings.PROJECT_PATH, 'HVZ', app, 'static', 'styles')
                if not os.path.exists(target_parent_dir):
                    os.mkdir(target_parent_dir, 755)

                target_dir = os.path.join(target_parent_dir, app)
                if not os.path.exists(target_dir):
                    os.mkdir(target_dir, 755)

                for source_path in glob.glob(os.path.join('styles', app, '*')):
                    subprocess.call([
                        'cp', '-R',
                        source_path,
                        os.path.join(settings.PROJECT_PATH, 'HVZ', app, 'static', 'styles', app),
                    ])

                subprocess.call([
                    'chmod', '-R', '755',
                    os.path.join(settings.PROJECT_PATH, 'HVZ', app, 'static', 'styles', app),
                ])
            except OSError:
                self.stderr.write("Unable to access the '{}' subapp.".format(app))
                continue

        os.chdir(self.old_dir)
        return
