from flask import Flask
from config import Config
from views.training import training_blueprint
from views.inference import inference_blueprint
from views.status import status_blueprint

app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(training_blueprint, url_prefix='/api')
app.register_blueprint(inference_blueprint, url_prefix='/api')
app.register_blueprint(status_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run()
