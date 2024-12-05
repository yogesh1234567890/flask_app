import os
from celery import Celery

CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')

def make_celery():
    celery = Celery(
        "tasks", 
        backend=CELERY_RESULT_BACKEND, 
        broker=CELERY_BROKER_URL,
    )
    return celery


celery = make_celery()


