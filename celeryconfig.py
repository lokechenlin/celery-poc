# Celery Settings
BROKER_URL = 'amqp://jsapi:q6tRadat@localhost/unittest2'
CELERY_RESULT_BACKEND = 'amqp://jsapi:q6tRadat@localhost/unittest2'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_ACCEPT_CONTENT=['json']

CELERY_TIMEZONE = 'Asia/Kuala_Lumpur'
CELERY_ENABLE_UTC = True

CELERYD_CONCURRENCY = 4

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'daemon.tasks.worker_daemon',
        'schedule': timedelta(seconds=30),
        'args': ()
    },
}

# Queue Settings
#QUEUES = ['general_queue', 'group*']
QUEUES = ['group*']


# Django Settings
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
