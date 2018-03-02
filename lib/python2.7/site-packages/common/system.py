"""
Use this function at very start of your script
which needs to work with django stuff.
Use it as first as possible to correctly initialize logging settings
(if you use django.settings.LOGGING feature)
"""
import os
import sys

def setup_django(script_file, relpath=None, module='settings'):
    ROOT = os.path.dirname(os.path.realpath(script_file))
    if relpath:
        ROOT = os.path.join(ROOT, relpath)
    os.chdir(ROOT)
    sys.path.insert(0, ROOT)
    os.environ['DJANGO_SETTINGS_MODULE'] = module

    from django.conf import settings

    # Force django.conf.settings calculation
    # This is required to initialize logging with settings
    # from django.conf.settings.LOGGING
    hasattr(settings, 'foo')
