from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialiga.settings')

app = Celery('socialiga')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.beat_schedule = {
#     'get_coins_data_from_coingecko_30s': {'task': 'coins.tasks.get_coins_data_from_coingecko', 'schedule': 60.0},
# }

# Load task modules from all registered Django app configs.

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.CELERY_TIMEZONE = 'UTC'
app.autodiscover_tasks()

# web: daphne moiwe.asgi:application --port $PORT --bind 0.0.0.0 -v2
# worker: python manage.py runworker --settings=moiwe.settings -v2

# celery -A moiwe worker -l INFO --concurrency 1 -P solo
# celery -A moiwe beat -l INFO
