# !/bin/bash

# Create a seed file for the first time

# Assumes that the container is called dynamicity-unm-web-1
sudo docker exec -it dynamicity-unm-web-1 /bin/bash -c "python3 manage.py dumpdata --exclude contenttypes --exclude auth.permission --indent 4 > /code/dynamiCITY_app/fixtures/seed.json"