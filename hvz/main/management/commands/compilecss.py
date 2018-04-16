import os
import subprocess

from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        main_static_dir = os.path.join(
            settings.BASE_DIR,
            'hvz',
            'main',
            'static',
        )

        subprocess.call([
            'compass',
            'compile',
            '--sass-dir', os.path.join(main_static_dir, 'sass'),
            '--css-dir', os.path.join(main_static_dir, 'styles'),
        ])

        print("Files compiled!")
