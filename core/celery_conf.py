import os
from datetime import timedelta

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')

app.autodiscover_tasks()
if settings.DEBUG:
    app.conf.broker_url = "redis://127.0.0.1:6379"
    app.conf.result_backend = "redis://127.0.0.1:6379"
else:
    app.conf.broker_url = "redis://redis:6379"
    app.conf.result_backend = "redis://redis:6379"
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['json', 'pickle']
app.conf.result_expires = timedelta(days=1)
app.conf.task_always_eager = False
app.conf.worker_prefetch_multiplier = 4
app.conf.beat_schedule = {
    'jobinja-every-30-minutes': {
        'task': 'main_module.tasks.fetch_data_from_jobinja',
        'schedule': 30.0 * 60,
    },
    'divar-every-30-minutes': {
        'task': 'main_module.tasks.fetch_data_from_divar',
        'schedule': 30.0 * 60,
    },
    'linkedin-every-1-hour': {
        'task': 'main_module.tasks.fetch_data_from_linkedin',
        'schedule': 30.0 * 60,
    },
    'daneshmandjobs-every-30-minutes': {
        'task': 'main_module.tasks.fetch_data_from_jobseeker',
        'schedule': 30.0 * 60,
    },
}
app.conf.timezone = 'UTC'
