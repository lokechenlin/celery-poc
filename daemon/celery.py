# celery worker -A daemon -l info 

from __future__ import absolute_import

from celery import Celery

app = Celery('daemon',
             broker=None,
             backend=None,
             include=['daemon.tasks'])

app.config_from_object('celeryconfig')

if __name__ == '__main__':
    app.start()

