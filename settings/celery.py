from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

from dotenv import load_dotenv
load_dotenv('.env')

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'settings.{os.getenv("ENVIRONMENT")}')

app = Celery('settings')  # Replace 'your_project' with your project's name.

# Configure Celery using settings from Django settings.py.
app.config_from_object(settings, namespace='CELERY')

# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Enable retrying connections on startup
app.conf.broker_connection_retry_on_startup = True

app.conf.timezone = 'Asia/Karachi'


app.conf.beat_schedule = {
    'main_scraping_process': {
        'task': 'scraping_scheduler.tasks.mobile_phone_scraping_scheduler',
        'schedule': 20 * 60,
        'args': (9355, False, False)
    },
    'mobile_scraping_process': {
        'task': 'scraping_scheduler.tasks.mobile_phone_scraping_scheduler',
        'schedule': crontab(hour=0, minute=0),
        'args': (9355, True, False)
    }
}