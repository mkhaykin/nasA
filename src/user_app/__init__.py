from flask import Flask

from shared.config import Config
from flask_login import LoginManager

from shared.tasks import init_scheduler

login_manager = LoginManager()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    init_scheduler()

    from user_app.routes import bp as user_bp

    app.register_blueprint(user_bp)

    return app
