from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hairsol.settings')
app = Celery('hairsol')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.task(bind=True, ignore_result=True)
