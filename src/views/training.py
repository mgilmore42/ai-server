from flask import Blueprint, jsonify

training_blueprint = Blueprint('training', __name__)

@training_blueprint.route('/train', methods=['POST'])
def train_model():
    return jsonify({"message": "Model training started."})
