"""Training view."""

from flask import Blueprint, Response, current_app, jsonify, request

training_blueprint = Blueprint('training', __name__)


@training_blueprint.route('/train', methods=['POST'])
def train_model() -> Response:
	"""TBD."""  # TODO: Add description
	current_app.logger.info('Model training started.')
	return jsonify({'message': 'Model training started.'})
