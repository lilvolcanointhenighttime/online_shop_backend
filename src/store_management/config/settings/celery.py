import os
from celery import Celery
from celery.schedules import crontab

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.store_management.config.settings')

app = Celery('store_management')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_expired_tokens_from_db': {
        'task': 'apps.users.tasks.delete_expired_tokens',
        'schedule': crontab(minute='*/1')
    }
}
