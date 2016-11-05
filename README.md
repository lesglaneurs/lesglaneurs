# How to set up a development environment

Clone the repository

    cd
    git clone https://github.com/lesglaneurs/lesglaneurs.git

Install the system dependencies

    # Imaging library
    sudo apt-get install libjpeg-dev
    # Geographic libraries
    sudo apt-get install binutils libproj-dev gdal-bin
    # Libray necessary to use Spatialite, the geographical extension of SQLite
    sudo apt-get install spatialite-bin

Create and activate a virtual environment

    sudo pip install virtualenv
    cd virtualenvs
    virtualenv lesglaneurs
    . lesglaneurs/bin/activate

Set up the project itself (let us assume your name is John Doe):

    cd ~/lesglaneurs
    pip install -r requirements.txt
    ./manage.py bower install
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser --username=johndoe --email=johndoe@gmail.com

Run the server:

    python manage.py runserver --settings=lesglaneurs.settings.dev

To check that the server is running, open your brower at the URL http://127.0.0.1:8000/local/admin/

# Reinstallation of pysqlite

Depending on the distros or on the environment, the loading of extensions may be forbidden in pysqlite2, the Python module used by Django to connect to SQLite.

Since we use the extension SpatiaLite, this lead to errors, typically when we try to migrate the database.

The error message is straightforward:

    raise ImproperlyConfigured('The pysqlite library does not support C extension loading. '
    django.core.exceptions.ImproperlyConfigured: The pysqlite library does not support C extension loading. Both SQLite and pysqlite must be configured to allow the loading of extensions to use SpatiaLite.

In that case, we must reinstall pysqlite2 as following:

    sudo apt-get install libsqlite3-dev
    cd /tmp
    wget ftp://ftp.uk.freesbie.org/sites/distfiles.finkmirrors.net/pysqlite-2.5.5.tar.gz
    gunzip pysqlite-2.5.5.tar.gz
    tar xvf pysqlite-2.5.5.tar
    cd pysqlite-2.5.5
    # Comment the line with 'define=SQLITE_OMIT_LOAD_EXTENSION' in setup.cfg
    python setup.py install

If it does not work, check first the directory containing the library:

    python -c 'import pysqlite2; import os; print os.path.dirname(pysqlite2.__file__)'

And then, check that all files have been updated by the installation, especially the .so.

# Addition of new packages

When you want to add a new external component, please follow below instructions.

Using pip :
    add the package and version in requirements.txt

Using bower :
    add the package in lesglaneurs/settings/settings.py, in BOWER_INSTALLED_APP
