### Celery Settings
BROKER_URL = 'amqp://jsapi:q6tRadat@localhost/unittest2'
CELERY_RESULT_BACKEND = 'amqp://jsapi:q6tRadat@localhost/unittest2'

# Define input and output format
CELERY_ACCEPT_CONTENT=['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Define Result Expires
CELERY_TASK_RESULT_EXPIRES = 60
CELERY_IGNORE_RESULT = True

# Define Timezone
CELERY_TIMEZONE = 'Asia/Kuala_Lumpur'
CELERY_ENABLE_UTC = True

# Define concurrency level
CELERYD_CONCURRENCY = 10

CELERY_ACKS_LATE = True

### Celery Scheduler Settings
from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'daemon.tasks.worker_daemon',
        'schedule': timedelta(seconds=30),
        'args': ()
    },
}

### Queue Settings, To be moved to json configuration under ./config/xxx
#QUEUES = ['general_queue', 'group*']
QUEUES = ['group*']

### Django Settings
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
