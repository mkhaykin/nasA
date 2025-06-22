from flask import Flask
from flask_wtf.csrf import CSRFProtect


from shared.config import Config

from shared.service import get_user, is_admin_exists, create_tables

from flask_login import LoginManager


login_manager = LoginManager()
csrf = CSRFProtect()


def create_app() -> Flask:
    create_tables()

    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.user_loader(get_user)
    login_manager.init_app(app)
    login_manager.login_view = "admin.login"

    csrf.init_app(app)

    from .setup import setup_bp

    app.register_blueprint(setup_bp)

    from .routes import bp as admin_bp

    app.register_blueprint(admin_bp)

    return app


def is_system_configured() -> bool:
    """Проверяет, выполнена ли начальная настройка"""
    return is_admin_exists()
