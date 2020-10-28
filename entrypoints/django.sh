#!/bin/bash

sleep 30 # hack to make sure that mysql is up and ready
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py seed
python manage.py runserver 0.0.0.0:8000