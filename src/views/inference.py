"""Inference view."""

import logging

from celery import Celery
from flask import Blueprint, Response, current_app, jsonify, request

logger = logging.getLogger(__name__)

inference_blueprint = Blueprint('inference', __name__)
inference_task_queue = Celery('inference', broker='pyamqp://guest@localhost//')


@inference_blueprint.route('/infer', methods=['POST'])
def perform_inference() -> Response:
	"""Performs inference.

	Parameters
	----------
	name : str
		The name of the model to perform inference with.
	version : str
		The version of the model to perform inference with.
	data : object
		The data to perform inference on.

	Returns
	-------
	Response
		The response containing the inference information.

	"""
	return process_inference(**request.json)


@inference_task_queue.task
def process_inference(name: str, user: str, version: str, data: object) -> Response:
	"""Processes inference request.

	Parameters
	----------
	name : str
		The name of the model to perform inference with.
	user : str
		The user requesting the inference.
	version : str
		The version of the model to perform inference with.
	data : object
		The data to perform inference on.

	Returns
	-------
	dict
		The response containing the inference information.

	"""
	current_app.logger.info(f'User: {user} requested inference for model {name}.')
	return jsonify({'model': name, 'version': version, 'user': user, 'data': data})
