from flask import Flask
from .config import configs
from .handlers import front

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    app.register_blueprint(front)

    return app
