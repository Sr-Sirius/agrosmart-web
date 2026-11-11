"""Application factory for the AgroSmart web application."""

from flask import Flask, render_template

from app.config import Config
from app.routes.main import main_bp
from app.routes.project import project_bp
from app.routes.monitoring import monitoring_bp
from app.routes.analytics import analytics_bp


def create_app(config_object=Config):
    """Create and configure a Flask application instance."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    app.register_blueprint(main_bp)
    app.register_blueprint(project_bp, url_prefix="/proyecto")
    app.register_blueprint(monitoring_bp, url_prefix="/monitoreo")
    app.register_blueprint(analytics_bp, url_prefix="/analitica")

    @app.errorhandler(404)
    def page_not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(_error):
        return render_template("errors/500.html"), 500

    return app
