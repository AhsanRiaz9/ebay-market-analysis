## Ebay Market Analysis
    
## Pre-Requisite:
- python3
- pip
- mysql

## Create Virtual Environment
 ### For windows:
    python -m venv venv

 ### For Linux:
    python3 -m venv venv

## Activate Virtual Environment
 ### For windows:
    venv/Scripts/activate

 ### For Linux:
    source venv/bin/activate


## Create .env file
- replace .env.example with .env
- Place your credentials in .env

## Install Required packages
    pip install -r requirements.txt

## Run Database migration
    python3 manage.py makemigrations
    python3 manage.py migrate

## Run Django Project:
    python3 manage.py runserver

Now, your django server will run at port 8000
http://127.0.0.1:8000/

If you face issue related to mysqlclient installation package use this documentation
https://pypi.org/project/mysqlclient/



## Run Celery Worker:
    python3 -m celery -A settings worker -B --loglevel=info -E


### Instruction to integerate Celery
    https://www.cherryservers.com/blog/how-to-install-and-start-using-rabbitmq-on-ubuntu-22-04
    https://medium.com/django-unleashed/how-to-use-celery-with-django-c4c341997704
    https://realpython.com/asynchronous-tasks-with-django-and-celery/

