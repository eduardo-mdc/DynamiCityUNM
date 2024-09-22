# !/bin/bash

python manage.py migrate
python manage.py flush
python manage.py loaddata dynamiCITY_app/fixtures/seed.json 
python manage.py runserver 0.0.0.0:8000