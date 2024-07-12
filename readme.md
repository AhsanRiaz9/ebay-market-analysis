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
    pip install - requirements.txt

## Run Database migration
    python3 manage.py makemigrations
    python3 manage.py migrate

## Run Django Project:
    python3 manage.py runserver

Now, your django server will run at port 8000
http://127.0.0.1:8000/

If you face issue related to mysqlclient installation package use this documentation
https://pypi.org/project/mysqlclient/
