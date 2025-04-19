import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WomenPeriodProjects.settings')

app = Celery('WomenPeriodProjects')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['WomenPeriodApp'])  # ¡Especifica tu app aquí!