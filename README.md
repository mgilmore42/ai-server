# AI Server

## Queue implementation using Celery

For implementing a queue into my project, I used Celery and py-amqp. Celery is a distributed task queue that is built on an asynchronous message passing system. It is focused on real-time operation, but supports scheduling as well. The execution units, called tasks, are executed concurrently on a single or more worker servers using multiprocessing, Eventlet, or gevent. Tasks can execute asynchronously (in the background) or synchronously (wait until ready).