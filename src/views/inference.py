from flask import Blueprint, jsonify

inference_blueprint = Blueprint('inference', __name__)

@inference_blueprint.route('/infer', methods=['POST'])
def perform_inference():
    return jsonify({"message": "Inference performed.", "result": "dummy_result"})
