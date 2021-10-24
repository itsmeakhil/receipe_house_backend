#!/bin/bash

echo "Starting RecipeHouse API Django application"
python3 manage.py collectstatic
export DJANGO_SETTINGS_MODULE="recipe_house_backend.settings"
gunicorn --workers=3 --bind=0.0.0.0:8000 recipe_house_backend.wsgi:application  --threads=3 --worker-connections=500 --log-level=debug --timeout=120
