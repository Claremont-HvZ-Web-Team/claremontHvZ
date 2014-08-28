#! /usr/bin/env python

from __future__ import print_function

import os
import sys
import subprocess

import optparse

def main():

    parser = optparse.OptionParser()
    parser.add_option(
        '--auto',
        help="Disable interactive terminal input",
        action="store_true",
        default=False,
    )
    parser.add_option(
        '--skipdeps',
        help="Skip dependency installation",
        action="store_true",
        default=False,
    )
    (options, args) = parser.parse_args()

    auto = options.auto
    skip_deps = options.skipdeps

    if not hasattr(sys, 'real_prefix'):
        print("Not inside a virtualenv! Run")
        print("    source bin/activate")
        print("from the root directory of your site to enter the virtualenv")
        return

    project_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'HVZ'
    )
    old_dir = os.getcwd()

    try:
        if not skip_deps:
            install_dependencies(project_path)

        copy_template_files(project_path)

        os.chdir(project_path)
        subprocess.call([
            'python',
            'manage.py',
            'setup-dev',
            ('--auto' if auto else ''),
        ])

    finally:
        os.chdir(old_dir)

def install_dependencies(project_path):
    print("Installing dependencies...", file=sys.stderr)
    delimit()

    print("Installing compass...", file=sys.stderr)
    subprocess.call([
        'sudo',
        'gem',
        'install',
        'compass',
    ])

    print("Installing requirements...", file=sys.stderr)
    subprocess.call([
        'pip',
        'install',
        '-r',
        os.path.join(os.path.dirname(project_path), 'dev-requirements.txt'),
        '--use-mirrors',
    ])


def copy_template_files(project_path):
    print("Copying template files...", file=sys.stderr)
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


def delimit():
    print("-" * 79, file=sys.stderr)

if __name__ == '__main__':
    main()
