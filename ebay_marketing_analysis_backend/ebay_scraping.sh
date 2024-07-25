source venv/bin/activate
python3 manage.py runserver 0.0.0.0:8008 & celery -A settings worker -B --loglevel=info -E