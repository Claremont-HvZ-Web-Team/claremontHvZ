Claremont Humans versus Zombies Site
====================================

This is the website for the Claremont College's biannual HvZ game.

Dev machine setup
-----------------

Developing for the site will require [Django] [4], [VirtualEnv] [3],
and [Compass] [6]. If you are familiar with and have (or know how to
get) all of these, feel free to skip this section.

First off, install [pip] [1] using your favorite package manager. If
you're developing on a Mac, I recommend installing/using [homebrew]
[2] as your package manager of choice. Then `brew install python` will
install pip.

Using pip, you should have an easy time installing virtualenv:

    pip install virtualenv

### Mac issue with Pip 1.3

There may be a compatibility issue with pip 1.3.x on Lion and Mountain
Lion. pip 1.3 requires SSL support, but Lion's version of Python has
an outdated OpenSSL library. The result is total brokeness. The [fix]
[5] is to reinstall Python through Homebrew, linking it to a newer
version of OpenSSL in the process.

Building the site
-----------------

Now create a root directory for your site. Mine is
`~/programming/claremonthvz.org`. I created two directories:
`~/programming/claremonthvz.org` and
`~/programming/claremonthvz.org/site`.

Note that I'm going to refer to `~/programming` everywhere in this
document. If your root directory is in a different place, substitute
accordingly.

Now build a virtualenv in the root directory, which for me was

    virtualenv ~/programming/claremonthvz.org

Clone your forked GitHub repo into the `site` directory (you don't
have to use the command line for this):

    git clone git@github.com:MYUSERNAME/claremontHvZ.git

And install the site's dependencies.

    cd ~/programming/claremonthvz.org/site/claremontHvZ
    pip install -r dev-requirements.txt

Some of the dependencies (like `django-localflavor-us`) exist in repos
on GitHub. You'll need to track these down and tell pip where they
are. For example, to install `django-localflavor-us`:

    pip install git+git://github.com/django/django-localflavor-us.git

If anyone figures out how to specify these in a requirements file,
that would be sweet.

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

    cd ~/programming/claremonthvz.org/site/claremontHvZ/HVZ/HVZ
    cp sample_local_settings.py local_settings.py

Moving passenger_wsgi.py
------------------------

Django relies on a file called `passenger_wsgi.py` to locate and load
the HVZ settings module and web specification library. Our production
server runs a more complicated one provided by DreamHost, but you can
just copy the simple development sample in the root directory:

    cd ~/programming/claremonthvz.org/site/claremontHvZ/HVZ
    cp sample_passenger_wsgi.py passenger_wsgi.py

Running the site
----------------

You control the site by running `manage.py`, found in
`site/claremontHvZ/HVZ`.

### Database synchronization

To initialize the database:

    python manage.py syncdb

You'll want to do this after every major change to `models.py`.

### Static file collection

To move the compiled images, stylesheets, and scripts to a `static` directory:

    python manage.py collectstatic

To compile static files:

    cd ~/programming/claremonthvz.org/site/static
    compass compile --sass-dir sass --css-dir styles


Haak wrote [a script] [7] to automatically compile the stylesheets
whenever new changes are merged in (Git will automatically run any
script `claremontHvZ/.git/hooks/post-merge` after every merge).

### Running a development version of the server

To run a development version of the server:

    python manage.py runserver

You can access the site by directing your browser to `localhost:8000`.

### Running unit tests

To run our unit tests:

    python manage.py main feed missions rules forums stats

The tests are fairly sparse right now, essentially making sure that
registration and feeding always work. Keep them up to date, and make
sure they all pass before you make a pull request.


[1]: http://www.pip-installer.org/ "PyPI Package Manager"
[2]: http://mxcl.github.io/homebrew/ "Homebrew"
[3]: https://pypi.python.org/pypi/virtualenv/ "VirtualEnv"
[4]: https://www.djangoproject.com/ "Django"
[5]: https://github.com/pypa/pip/issues/829/ "pip Issue 829"
[6]: https://rubygems.org/gems/compass "Compass"
[7]: https://github.com/haaksmash/tools/blob/master/githooks/deploy/post-merge "Haak's Post-Merge Hook"
