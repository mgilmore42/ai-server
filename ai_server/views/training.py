"""Training view."""

from ..database.database import Database
from celery import Celery
from flask import Blueprint, Response, current_app, jsonify, request

training_blueprint = Blueprint('training', __name__)
training_task_queue = Celery('training', broker='pyamqp://guest@localhost//')


@training_blueprint.route('/train', methods=['POST'])
def train_model() -> Response:
	"""Trains a model.

	Parameters
	----------
	name : str
		The name of the model to train.
	task : str
		The task the model is intended for.
	dataset : str
		The dataset to train the model on.
	username : str
		The username of the user requesting the training.
	version : str
		The version of the model to train.

	Returns
	-------
	Response
		The response containing the model training information.

	"""
	return process_model(**request.json)


@training_blueprint.route('/add_model', methods=['POST'])
def add_model() -> Response:
	"""Adds a model to the database.

	Parameters
	----------
	name : str
		The name of the model to train.
	task : str
		The task the model is intended for.

	Returns
	-------
	Response
		The response containing the model training information.

	"""
	return process_model_addition(**request.json)


@training_blueprint.route('/add_task', methods=['POST'])
def add_task() -> Response:
	"""Adds a task to the database.

	Parameters
	----------
	task : str
		The name of the task to add.

	Returns
	-------
	Response
		The response containing the task information.

	"""
	return process_task_addition(**request.json)


@training_task_queue.task
def process_model(
	name: str, username: str, version: str
) -> Response:
	"""Processes a model training request.

	Takes the model training request interfaces with the database the queue system to process the request.

	Parameters
	----------
	name : str
		The name of the model to train.
	username : str
		The username of the user requesting the training.
	version : str
		The version of the model to train.

	Returns
	-------
	dict
		The response containing the model training information.

	"""
	current_app.logger.info(f'User: {username} requested training for model {name}.')

	database = Database()

	result = database.train_model(name, username, version)

	database.close()

	return jsonify(result)


@training_task_queue.task
def process_model_addition(
	name: str, task: str
) -> Response:
	"""Processes a model training request.

	Takes the model training request interfaces with the database the queue system to process the request.

	Parameters
	----------
	name : str
		The name of the model to train.
	task : str
		The task the model is intended for.

	Returns
	-------
	dict
		The response containing the model training information.

	"""
	current_app.logger.info(f'Adding model {name} for task {task}.')

	database = Database()

	result = database.add_model(name, task)

	database.close()

	return jsonify(result)


@training_task_queue.task
def process_task_addition(
	task: str
) -> Response:
	"""Processes a task addition request.

	Takes the task addition request interfaces with the database the queue system to process the request.

	Parameters
	----------
	task : str
		The name of the task to add.

	Returns
	-------
	dict
		The response containing the task information.

	"""
	current_app.logger.info(f'Adding task {task}.')

	database = Database()

	result = database.add_task(task)

	database.close()

	return jsonify(result)
