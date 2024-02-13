"""Training view."""

from flask import Blueprint, Response, current_app, jsonify, request

training_blueprint = Blueprint('training', __name__)


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
	return jsonify(**request.json)


def process_model(
	name: str, task: str, dataset: str, username: str, version: str
) -> dict:
	"""Processes a model training request.

	Takes the model training request interfaces with the database the queue system to process the request.

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
	dict
		The response containing the model training information.

	"""
	current_app.logger.info(f'User: {username} requested training for model {name}.')

	return jsonify(
		{
			'model': name,
			'task': task,
			'dataset': dataset,
			'user': username,
			'version': version,
		}
	)
