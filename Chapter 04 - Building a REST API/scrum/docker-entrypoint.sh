#!/bin/bash

python manage.py migrate auth
python manage.py createsuperuser --noinput
python manage.py makemigrations board
python manage.py migrate board

exec "$@"