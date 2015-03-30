********************************************************************
Installation
********************************************************************
## Get standard lib
sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel<br>

## Get Python
(http://g0o0o0gle.com/install-python-3-4-1-centos-6/) <br>
cd /usr/local/src<br>
sudo wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tar.xz<br>

## Extract and Install
tar -xJf Python-3.4.3.tar.xz<br>
cd Python-3.4.3<br>
sudo ./configure --prefix=/usr/local -enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"<br>
sudo make<br>
sudo make altinstall<br>

## Install easy_install : easy_install --help or 
(https://pythonhosted.org/setuptools/easy_install.html#using-easy-install)<br>
sudo wget https://bootstrap.pypa.io/ez_setup.py<br>
sudo python3.4 ez_setup.py<br> 

## Install Django
python3.4 -m easy_install "Django==1.7.6"<br>

## Install celery
python3.4 -m easy_install celery<br>

## Install pika as rabbitmq client
python3.4 -m easy_install "pika==0.9.8"<br>

## Install requests module
python3.4 -m easy_install requests<br>

## Install memcahced
python3.4 -m easy_install python-memcached <br>


********************************************************************
Command to run this program
********************************************************************
cd ../celery-poc<br>

## Start Monitoring: After that, Go to http://localhost:5555/
celery flower --broker=amqp://jsapi:xxxxxx@locaost:5672/unittest2 --port=5555<br>

## Start Worker
celery worker -A daemon -l info --concurrency=5 --purge --autoscale=10,5<br>

## Start Scheduler
celery -A daemon beat<br>

## Example to call a task
celery call daemon.tasks.worker_daemon<br>


