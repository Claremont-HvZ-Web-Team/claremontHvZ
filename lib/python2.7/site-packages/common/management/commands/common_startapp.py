from optparse import make_option
from os.path import dirname, realpath
import os.path
import shutil

from django.core.management.base import BaseCommand, CommandError

COMMON_ROOT = dirname(dirname(dirname(realpath(__file__))))
SKELETON_PATH = os.path.join(COMMON_ROOT, 'data', 'app_template')

class Command(BaseCommand):
    help = 'Create django application skeleton'

    def handle(self, *args, **kwargs):
        if not args:
            raise Exception('Application name required')
        app_name = args[0]
        if os.path.exists(app_name):
            raise Exception('Directory with such name exists')
        copydir(SKELETON_PATH, app_name)


def copydir(src, dst):
    if not os.path.exists(dst):
        print 'Creating directory: %s' % dst
        os.mkdir(dst)
    else:
        print 'Directory already exists: %s' % dst

    for fname in os.listdir(src):
        src_path = os.path.join(src, fname)
        dst_path = os.path.join(dst, fname)
        if os.path.isdir(src_path):
            copydir(src_path, dst_path)
        else:
            print 'Creating file: %s' % dst_path
            shutil.copy(src_path, dst_path)
