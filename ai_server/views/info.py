"""Status view."""

from ..database.database import Database

from celery import Celery
from flask import Blueprint, Response, current_app, jsonify, request

info_blueprint = Blueprint('status', __name__)
info_task_queue = Celery('status', broker='pyamqp://guest@localhost//')


@info_blueprint.route('/info/user', methods=['GET'])
def get_user() -> Response:
	"""Get information on a user.

	Parameters
	----------
	username : str
		The username to get information on.

	Returns
	-------
	Response
		The response containing the user information.

	"""
	return get_user_info(**request.json)


@info_blueprint.route('/info/model', methods=['GET'])
def get_model() -> Response:
	"""Get information on a model.

	Parameters
	----------
	model : str
		The model to get information on.
	version : str
		The version of the model to get information on.

	Returns
	-------
	Response
		The response containing the model information.

	"""
	return get_model_info(**request.json)


@info_task_queue.task
def get_user_info(username: str) -> Response:
	"""Get information on a user.

	Query the user registry for information on the selected user.
	Currently, this function returns a dummy response.

	Parameters
	----------
	username : str
		The username to get information on.

	Returns
	-------
	dict
		The response containing the user information.

	"""
	current_app.logger.info(f'Checking status for user {username}.')

	database = Database()

	user = database.get_user(username)

	database.close()

	return jsonify(user)


@info_task_queue.task
def get_model_info(model: str, version: str) -> Response:
	"""Get information on a model.

	Query the model registry for information on the specified model and version.
	Currently, this function returns a dummy response.

	Parameters
	----------
	model : str
		The model to get information on.
	version : str
		The version of the model to get information on.

	Returns
	-------
	dict
		The response containing the model information.

	"""
	current_app.logger.info(f'Checking status for model {model} version {version}.')

	database = Database()

	model = database.get_model(model, version)

	database.close()

	return jsonify({'model': model, 'version': version})
