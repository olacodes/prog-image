import os
import environ
from celery import Celery

env = environ.Env()

app = Celery('app')
app.conf.broker_url = env("CELERY_BROKER_URL", default='redis://redis:6379/0')
app.conf.result_backend = env("CELERY_RESULT_BACKEND", default="redis://redis:6379/0")
app.conf.imports = ['storage_service.app.tasks']
# app.conf.imports = ['process_service.filtering.filter']
# app.conf.task_serializer = 'pickle'
# app.conf.result_serializer = 'pickle'
# app.conf.accept_content = ['application/json',
#                            'application/x-python-serialize']

app.autodiscover_tasks()
