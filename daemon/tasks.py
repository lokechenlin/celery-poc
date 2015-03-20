from __future__ import absolute_import

from daemon.celery import app
from kombu import Connection
from celery.utils.log import get_task_logger
from django.core.cache import cache
from celery.result import AsyncResult

import requests
import time
import json   


@app.task
def abc():
    x = cde.delay() 
    print("start") 
    print(x) 
    print(x.task_id)
    print("end") 
    return True

@app.task
def cde():
    return True

# celery call daemon.tasks.worker_daemon
@app.task
def worker_daemon():
    # A worker daemon will get the queue listing, config to be handled and call the parent worker.
    
    # http://celery.readthedocs.org/en/latest/tutorials/task-cookbook.html#cookbook-task-serial
    # http://loose-bits.com/2010/10/distributed-task-locking-in-celery.html

    # First of all, make sure it run once
    LOCK_EXPIRE = 60 * 5 # Lock expires in 5 minutes
    lock_id = 'worker_daemon'
    # cache.add fails if if the key already exists
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    # memcache delete is very slow, but we have to use it to take
    # advantage of using add() for atomic locking
    release_lock = lambda: cache.delete(lock_id)
    
    if acquire_lock():
        print('START spawning parent worker ...') 
    else:
        print('Do not start spawning parent worker because duplicate task...')         
        return False  

    try:
        # Load Configuration
        json_data = open('./config/queues.json').read()
        json_config = json.loads(json_data)

        # Loop through list of predefined queue.
        for item in app.conf.QUEUES:

            # Get the queue configuration
            queue_config = json_config[item]
            
            # Check if group queue or general queue
            if item[-1] == '*':
                # Todo: Check if group_worker is running?

                print ("Calling group_worker for " + item[:-1])
                group_worker.delay(item[:-1], queue_config)        
            else:
                # Todo: Check if general_worker is running?

                print ("Calling general_worker for " + item)
                general_worker.delay(item, queue_config)
    finally:
        print ('END. Worker daemon is done!')
        release_lock()   

    return True


@app.task
def general_worker(queue_name, queue_config):
    # A general worker call task by managing the concurrency 

    # First of all, make sure it run once
    LOCK_EXPIRE = 60 * 5 # Lock expires in 5 minutes
    lock_id = 'general_worker_' + queue_name
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)
    
    if acquire_lock():
        print('START general worker ... ' + queue_name) 
    else:
        print('Duplicate task. Do not start general worker ... ' + queue_name)         
        return False  
    
    try:
        # Retrieve the concurrency level 
        concurrency_level = 1    

        for i in range(0, concurrency_level):
        
            # Todo: Check the status of task
        
            # Call Task to process message
            x = do_task.delay(queue_name, queue_config)

            # Todo: Loop and monitor the task
    finally:
        print ('END. General worker is done!')  
        release_lock() 
    
    return True


# celery call daemon.tasks.group_worker --args='["group",{"max_idle_seconds": 0}]' 
@app.task
def group_worker(queue_name_prefix, queue_config):
    # A group worker call queue API and call task.

    # First of all, make sure it run once
    LOCK_EXPIRE = 60 * 5 # Lock expires in 5 minutes
    lock_id = 'group_worker_' + queue_name_prefix
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)
    release_lock() 
    if acquire_lock():
        print('START group worker ... ' + queue_name_prefix) 
    else:
        print('Duplicate task. Do not start group worker ... ' + queue_name_prefix)         
        return False  

    try:
        while True:
            # Call the RabbitMQ API
            api_rabbitmq = 'http://jsapi:q6tRadat@localhost:15672/api/queues/unittest2?columns=name,consumers'
            response = requests.get(api_rabbitmq)
            data = response.json()
            #print ("Queue list: %s" % data)
          
            # Loop thru queue available and spawn task
            for item in data:
                prefix_len = len(queue_name_prefix)
                try:
                    consumer = item['consumers']    
                except IndexError:
                    continue
                
                try:
                    name = item['name']
                except IndexError:
                    continue

                name_len = len(name) 
                
                if (prefix_len < name_len 
                    and name[0:prefix_len] == queue_name_prefix 
                    and consumer == 0):
                    
                    # Define Lock ID
                    lock_id = 'do_task_' + name
                    
                    # Check Current Task Status
                    task_id = cache.get(lock_id)                         
                    if task_id != None:
                        state = AsyncResult(task_id).state                   
                    else:
                        state = None 
                    
                    print ("Task %s STATUS = %s" % (task_id, state)) 

                    if state == 'SUCCESS' or state == None:
                        print ("Spawning Group Task: %s" % name)
                        x = do_task.delay(name, queue_config)       
                        cache.set(lock_id, x.task_id)
                
            time.sleep(10)
    finally:
        print ('END. Group worker is done!')   
        release_lock() 

    return True


# celery call daemon.tasks.do_task --args='["general_queue",{"max_idle_seconds": 0}]' 
@app.task
def do_task(queue_name, queue_config):
    # A common task worker to listen to a queue, call to API, 
    # store log, and reply messages with proper error Handling is needed.
    print('START doing task ...' + queue_name)

    # Read Config
    try:
        max_idle_seconds = queue_config['max_idle_seconds']
    except IndexError:
        max_idle_seconds = 0    
    
    # http://kombu.readthedocs.org/en/latest/userguide/examples.html
    with Connection('amqp://jsapi:q6tRadat@localhost:5672/unittest2') as conn:
        
        # Open Channel
        simple_queue = conn.SimpleQueue(queue_name)  

        while True:

            # Retrieve Message                          
            try:
                message = simple_queue.get(block=True, timeout=1)
            except Exception:            
                message = ''
                pass

            if message == '' or message == None:               
                if max_idle_seconds == 0:
                    print("No more message ... end")  
                    return True
                else:
                    print("No more message ... sleep 5")       
                    time.sleep(5)
            else:
                print("Message received: %s" % message.payload)
                print("Message properties: %s" % message.properties)    
                        
                # Call API
                api = 'http://tick.jobstreet.com/~chenlin/celery-test-api.php'
                print("Fire to RESTful API: %s" % api)                
                response = requests.get(api)
                data = response.json()
                print ("RESTful API Response: %s" % data)

                # Todo: Log
                # Reply to
                try:
                    reply_to = message.properties['reply_to']
                except IndexError:
                    reply_to = None

                if reply_to != '' and reply_to != None:
                    publisher = conn.SimpleQueue(message.properties['reply_to'])
                    publisher.put(data)
                    publisher.close()        
                   
                # Ack Message
                message.ack() 

            print ("Next message ... ")                

        # Close Channel
        simple_queue.close()

    print ('END. Task is done!')
    return True

# celery call daemon.tasks.do_task --args='["general_queue",{"max_idle_seconds": 0}]' 
@app.task
def sample_task(queue_name, queue_config):    

    with Connection('amqp://jsapi:q6tRadat@localhost:5672/unittest2') as conn:
        
        # Open Channel
        simple_queue = conn.SimpleQueue(queue_name)  

        while True:
            # Retrieve Message                          
            message = simple_queue.get(block=True, timeout=1)
           
            if message == '' or message == None:               
                print("No more message ... end")  
                return True
                
            else:
                print("Message received: %s" % message.payload)
                        
                # Call API
                api = 'http://tick.jobstreet.com/~chenlin/celery-test-api.php'                           
                response = requests.get(api)
                data = response.json()                
   
                # Ack Message
                message.ack() 

            print ("Next message ... ")                

        # Close Channel
        simple_queue.close()

    return True
