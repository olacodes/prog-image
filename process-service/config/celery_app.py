import os
import environ
from celery import Celery

env = environ.Env()

app = Celery('compression')
app.conf.broker_url = env("CELERY_BROKER_URL")
app.conf.result_backend = env("CELERY_RESULT_BACKEND")
# app.conf.imports = ['app.tasks']
# app.conf.task_serializer = 'pickle'
# app.conf.result_serializer = 'pickle'
# app.conf.accept_content = ['application/json',
#                            'application/x-python-serialize']

app.autodiscover_tasks()
