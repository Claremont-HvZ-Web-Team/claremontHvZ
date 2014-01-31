Claremont Humans versus Zombies Site
====================================

This is the website for the Claremont College's biannual HvZ game.

Dev machine setup
-----------------

Developing for the site will require [Django] [4], [VirtualEnv] [3],
and [Compass] [5]. If you are familiar with and have (or know how to
get) all of these, feel free to skip this section.

First off, install [pip] [1] using your favorite package manager. If
you're developing on a Mac, I recommend installing/using [homebrew]
[2] as your package manager of choice. Then `brew install python` will
install pip.

Using pip, you should have an easy time installing virtualenv:

    pip install virtualenv

Building the site
-----------------

Now create a root directory for your site. Mine is
`~/programming/claremonthvz.org`.

Note that I'm going to refer to `~/programming` everywhere. If your
root directory is in a different place, use your imagination and
substitute accordingly.

### Setting up the Virtual Environment

Now build a virtualenv in the root directory, which for me was

    virtualenv ~/programming/claremonthvz.org

A virtualenv provides a wrapper between the site and your machine. As
long as the site only interacts with code from within this wrapper, we
ensure that the site will work on anyone's machine.

You won't actually be _using_ the virtualenv until you activate it:

    source ~/programming/claremonthvz.org/bin/activate

This needs to be run every time you start up a terminal to work on the
site. I recommend you add the following alias to your .bashrc:

    alias hvz="cd ~/personal-projects/claremonthvz.org && source bin/activate && cd claremontHvZ/HVZ"

Then you can just type `hvz` when you want to start hacking away.

### Git clone!

Clone your forked GitHub repo (you don't have to use the command line
for this):

    git clone git@github.com:MYUSERNAME/claremontHvZ.git

And install the site's dependencies.

    cd ~/programming/claremonthvz.org/claremontHvZ
    pip install -r dev-requirements.txt

To compile stylesheets, we use Compass.

    gem install compass

Specifying settings
-------------------

The site has two settings files. One file, called `settings.py`, is
supposed to stay constant for our site. The other file, called
`local_settings.py`, contains data that is secret or specific to a
particular machine or both. You'll need to create this file. You can
start by copying the sample `local_settings_sample.py` we've provided
for you:

    cd ~/programming/claremonthvz.org/claremontHvZ/HVZ/HVZ
    cp sample_local_settings.py local_settings.py

Running the site
----------------

You control the site by running `manage.py`, found in
`claremontHvZ/HVZ`.

### Database synchronization

To initialize the database:

    python manage.py syncdb

You'll want to do this after every major change to `models.py`.

### Loading colleges data

To load data about the Claremont Colleges:

    python manage.py loaddata HVZ/main/fixtures/production.json

### Static file collection

To move the compiled images, stylesheets, and scripts to a `static` directory:

    python manage.py collectstatic

To compile static files:

    cd ~/programming/claremonthvz.org/HVZ/HVZ/main/static
    compass compile --sass-dir sass --css-dir styles

If you're working on the style files, keep a terminal running
`compass watch`. This will continually check for changes to
your stylesheets.

### Running unit tests

If you've followed all of the above steps, all unit tests should pass:

    python manage.py test HVZ

These tests check registration, feeding, and permission scenarios ---
they've saved my ass many a time. Run them before committing code!

### Running a development version of the server

To run a development version of the server:

    python manage.py runserver

You can then access the site by directing your browser to `localhost:8000`.


[1]: http://www.pip-installer.org/ "PyPI Package Manager"
[2]: http://mxcl.github.io/homebrew/ "Homebrew"
[3]: https://pypi.python.org/pypi/virtualenv/ "VirtualEnv"
[4]: https://www.djangoproject.com/ "Django"
[5]: https://rubygems.org/gems/compass "Compass"
