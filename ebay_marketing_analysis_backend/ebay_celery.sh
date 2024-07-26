source venv/bin/activate
celery -A settings worker -B --loglevel=info -E