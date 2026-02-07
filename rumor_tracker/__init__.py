from flask import Flask
from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # import models
    from .models import user, rumour, report  # noqa: F401

    # register controllers
    from .controllers.rumours_controller import rumours_bp
    from .controllers.reports_controller import reports_bp
    from .controllers.summary_controller import summary_bp

    app.register_blueprint(rumours_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(summary_bp)

    return app
