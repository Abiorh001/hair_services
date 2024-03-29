#!/bin/bash

# bash script to install gunicorn and start the django application server

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# check if gunicorn is already installed then skip installation
if [ -x "$(command -v gunicorn)" ]; then
    echo "Gunicorn already installed. Skipping installation."
    gunicorn hair_services.wsgi:application -b 0.0.0.0:8000
    exit 0
elif command -v apt-get &> /dev/null; then
    # install gunicorn
    apt-get update -y && apt-get install gunicorn -y

    # Start the production server
    gunicorn hair_services.wsgi:application -b 0.0.0.0:8000
else
    echo "Package manager not found. Please install gunicorn manually."
    exit 1
fi
