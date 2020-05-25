# Bangazon E-Commerce Site
### This is the server side of the application, built with Django REST.
### To view the client side repository (built with ReactJS), visit: https://github.com/sampita/bangazon-client-virtual-magicians-1

Contributors to this project:
- Guy Cherkesky
- Julian Garcia
- John Long
- Sam Pita

____________________________

## Installation Instructions

### Create the django app
django-admin startproject virtual-magicians-api

### Create Virtual Enviroment
python -m venv virtual-magicians-api  
source ./virtual-magicians-api/bin/activate

### Install Require Package
pip install django autopep8 pylint djangorestframework django-cors-headers pylint-django

pip freeze > requirements.txt

### Create Django Table
python manage.py migrate

### Create API App
python manage.py startapp virtual-magicians-api

### Run Server
python manage.py runserver
