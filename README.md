********************************************************************
Installation
********************************************************************
## Get standard lib
sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel

## Get Python
## http://g0o0o0gle.com/install-python-3-4-1-centos-6/
cd /usr/local/src
sudo wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tar.xz

## Extract and Install
tar -xJf Python-3.4.3.tar.xz
cd Python-3.4.3
sudo ./configure --prefix=/usr/local -enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
sudo make
sudo make altinstall

## Install easy_install : easy_install --help or 
## https://pythonhosted.org/setuptools/easy_install.html#using-easy-install
sudo wget https://bootstrap.pypa.io/ez_setup.py
sudo python3.4 ez_setup.py 

## Install Django
python3.4 -m easy_install "Django==1.7.6"

## Install celery
python3.4 -m easy_install celery

## Install pika as rabbitmq client
python3.4 -m easy_install "pika==0.9.8"

## Install requests module
python3.4 -m easy_install requests

## Install memcahced
python3.4 -m easy_install python-memcached 


********************************************************************
Command to run this program
********************************************************************
cd ../celery-poc

## Start Monitoring: After that, Go to http://localhost:5555/
celery flower --broker=amqp://jsapi:xxxxxx@locaost:5672/unittest2 --port=5555

## Start Worker
celery worker -A daemon -l info 

## Start Scheduler
celery -A daemon beat

## Example to call a task
celery call daemon.tasks.worker_daemon


