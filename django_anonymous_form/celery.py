import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_anonymous_form.settings')

app = Celery('django_anonymous_form')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# celery beat tasks

app.conf.beat_schedule = {
}

# C:\projects\django_page_calculator\venv\Scripts\python.exe C:\projects\django_page_calculator\venv\Scripts\celery.exe -A django_page_calculator worker -l info --pool=solo