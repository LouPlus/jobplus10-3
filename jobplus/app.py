from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import configure_uploads, patch_request_class

from jobplus.forms import rfile, clogo
from .config import configs
from jobplus.models import db, User


def register_blueprints(app):
    from .handlers import front, user, company, job
    app.register_blueprint(front)
    app.register_blueprint(user)
    app.register_blueprint(company)
    app.register_blueprint(job)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    configure_uploads(app, (rfile, clogo))
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'

