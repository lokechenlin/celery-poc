# celery worker -A daemon -l info 

from __future__ import absolute_import

from celery import Celery

app = Celery('daemon',
             broker='amqp://jsapi:q6tRadat@localhost/unittest2',
             backend='amqp://jsapi:q6tRadat@localhost/unittest2',
             include=['daemon.tasks'])

app.config_from_object('celeryconfig')

if __name__ == '__main__':
    app.start()

