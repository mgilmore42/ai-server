"""Status view."""

from flask import Blueprint, Response, current_app, jsonify

status_blueprint = Blueprint('status', __name__)


@status_blueprint.route('/status', methods=['GET'])
def check_status() -> Response:
	"""TBD."""  # TODO: Add description
	current_app.logger.info('Status checked.')

	return jsonify({'message': 'Status checked.', 'status': 'In progress'})
