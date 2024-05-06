# AI Server

## Installation

This package is managed using poetry. In order to install you need a python version >= 3.10. To install simply run:

```bash
pip install git+https://github.com/mitch-gilmore/ai-server.git
```

There is a build in CLI utility that can be used to start the server. To start the server run:

```bash
ai-server
```

Then the Flask server will be running on `http://localhost:5000` and read to server RESTful API requests.

## Queue implementation using Celery

For implementing a queue into my project, I used Celery and py-amqp. Celery is a distributed task queue that is built on an asynchronous message passing system. It is focused on real-time operation, but supports scheduling as well. The execution units, called tasks, are executed concurrently on a single or more worker servers using multiprocessing, Eventlet, or gevent. Tasks can execute asynchronously (in the background) or synchronously (wait until ready).

## SQL Injection protection

To protect against SQL injection, I use sqlite3 and the `execute` method. The `execute` method is used to execute a SQL query. The query is passed as a string to the `execute` method. The `execute` method will then execute the query on the database. The `execute` method will automatically escape any special characters in the query string, which will prevent SQL injection attacks.