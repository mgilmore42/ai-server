"""Inference view."""

import logging

from flask import Blueprint, Response, jsonify

logger = logging.getLogger(__name__)

inference_blueprint = Blueprint('inference', __name__)


@inference_blueprint.route('/infer', methods=['POST'])
def perform_inference() -> Response:
	"""TBD."""  # TODO: Add description
	logger.info('Inference performed.')
	return jsonify({'message': 'Inference performed.', 'result': 'dummy_result'})
