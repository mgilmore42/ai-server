"""Main application file for the Flask API."""

from .config import Config
from flask import Flask
from .database.database import Database
from .views.inference import inference_blueprint
from .views.info import info_blueprint
from .views.training import training_blueprint

def run():
	app = Flask(__name__)
	app.config.from_object(Config)

	# add database to the app
	# setattr(app, 'database', Database())

	# Register Blueprints
	app.register_blueprint(training_blueprint, url_prefix='/api')
	app.register_blueprint(inference_blueprint, url_prefix='/api')
	app.register_blueprint(info_blueprint, url_prefix='/api')

	app.run()

if __name__ == '__main__':
	run()
