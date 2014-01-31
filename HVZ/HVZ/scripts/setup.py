#! /usr/bin/env python

import os
import sys
import subprocess

def main():
    if not hasattr(sys, 'real_prefix'):
        print("Not inside a virtualenv! Run")
        print("    source bin/activate")
        print("from the root directory of your site to enter the virtualenv")
        return

    project_path = os.path.abspath(__file__)
    for i in range(3):
        project_path = os.path.dirname(project_path)

    old_dir = os.getcwd()

    try:
        print("Installing dependencies...")
        delimit()

        subprocess.call([
            'gem',
            'install',
            'compass',
        ])

        subprocess.call([
            'pip',
            'install',
            '-r',
            os.path.join(os.path.dirname(project_path), 'dev-requirements.txt'),
        ])
        
    finally:
        os.chdir(old_dir)

    try:
        print("Copying template files...")
        delimit()

        files = 0

        os.chdir(os.path.join(project_path, 'HVZ'))
        if not os.path.exists('local_settings.py'):
            print("local_settings.py...")
            subprocess.call([
                'cp',
                'sample_local_settings.py',
                'local_settings.py',
            ])
            files += 1

        os.chdir(os.path.join(project_path))
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

    try:
        os.chdir(project_path)

        subprocess.call([
            'python',
            'manage.py',
            'setup-dev',
        ])

    finally:
        os.chdir(old_dir)

def delimit():
    print("-" * 79)

if __name__ == '__main__':
    main()
