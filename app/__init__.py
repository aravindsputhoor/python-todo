from flask import Flask
from .config import Config
from .models import db
from .routes import api


def create_app(config_class=Config):
    app = Flask(__name__)

    # Load base or custom config
    if isinstance(config_class, type):
        app.config.from_object(config_class)
    elif isinstance(config_class, dict):
        app.config.from_object(Config)
        app.config.update(config_class)

    db.init_app(app)
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    return app