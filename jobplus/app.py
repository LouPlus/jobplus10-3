from flask import Flask
from flask_migrate import Migrate

from .config import configs
from .handlers import front
from jobplus.models import db


def register_blueprints(app):
    from .handlers import front
    app.register_blueprint(front)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    # db.init_app(app)
    # Migrate(app, db)
    register_blueprints(app)

    return app

