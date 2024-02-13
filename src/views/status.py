from flask import Blueprint, jsonify

status_blueprint = Blueprint('status', __name__)

@status_blueprint.route('/status', methods=['GET'])
def check_status():
    return jsonify({"message": "Status checked.", "status": "In progress"})
