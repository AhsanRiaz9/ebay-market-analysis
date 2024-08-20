cd ebay_marketing_analysis_backend/
source venv/bin/activate
celery -A settings worker -B --loglevel=info -E