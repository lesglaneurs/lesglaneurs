#!/bin/bash

## sudo gunicorn lesglaneurs.wsgi:application --bind 127.0.0.1:5555


NAME="lesglaneurs_fullcalendar"     
PROJECT_NAME=lesglaneurs                       # Name of the application
DJANGO_DIR=/webapps/django/lesglaneurs_fullcalendar          # Django project directory
SOCKFILE=/webapps/django/run/gunicorn_fullcalendar.sock        # to handled shared file system with VM
USER=django                                       # the user to run as
GROUP=webapps                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings.dev
DJANGO_WSGI_MODULE=$PROJECT_NAME.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
# cd $DJANGODIR			
# source ../bin/activate		
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
# export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --user=$USER --group=$GROUP \
  --workers $NUM_WORKERS \
  --bind=unix:$SOCKFILE \
  --log-level=info \
  --log-file=$DJANGO_DIR/run/logs/gunicorn.log \
