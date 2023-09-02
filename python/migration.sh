#!/bin/bash

python3 manage.py makemigrations advertise
python3 manage.py makemigrations cart
python3 manage.py makemigrations login
python3 manage.py makemigrations merchant
python3 manage.py makemigrations order
python3 manage.py makemigrations photo
python3 manage.py makemigrations stock

python3 manage.py migrate




