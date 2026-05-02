#!/usr/bin/env bash
# exit on error
set -o errexit

# Clear cache
find . -path "*/__pycache__/*" -delete
find . -name "*.pyc" -delete

pip install -r requirements.txt

python manage.py collectstatic --no-input
rm -f db.sqlite3
python manage.py makemigrations lands
python manage.py migrate
python seed_lands.py
