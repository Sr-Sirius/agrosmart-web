"""Application factory for the AgroSmart web application."""

from flask import Flask, render_template, request, url_for

from app import content
from app.config import Config
from app.routes.main import main_bp
from app.routes.project import project_bp
from app.routes.monitoring import monitoring_bp
from app.routes.analytics import analytics_bp
from app.routes.results import results_bp


def _sequence_neighbors(endpoint):
    """Return the previous and next pages of the reading order."""
    keys = [item[0] for item in content.SECUENCIA]
    if endpoint not in keys:
        return None, None
    index = keys.index(endpoint)
    previous = content.SECUENCIA[index - 1] if index > 0 else None
    following = content.SECUENCIA[index + 1] if index < len(keys) - 1 else None
    return previous, following


def create_app(config_object=Config):
    """Create and configure a Flask application instance."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    app.register_blueprint(main_bp)
    app.register_blueprint(project_bp, url_prefix="/proyecto")
    app.register_blueprint(monitoring_bp, url_prefix="/monitoreo")
    app.register_blueprint(analytics_bp, url_prefix="/analitica")
    app.register_blueprint(results_bp, url_prefix="/resultados")

    if app.config.get("ENABLE_DEVICE_API"):
        from app.routes.live import registrar
        registrar(app)

    @app.context_processor
    def inject_site_content():
        previous, following = _sequence_neighbors(request.endpoint)
        return {
            "c": content,
            "menu": content.MENU,
            "seq_prev": previous,
            "seq_next": following,
            "powerbi_embed_url": app.config.get("POWERBI_EMBED_URL", ""),
            "live_enabled": bool(app.config.get("ENABLE_DEVICE_API")),
        }

    @app.template_filter("miles")
    def miles(value, decimals=0):
        """Format numbers with Spanish separators: 1.234,56."""
        text = f"{value:,.{decimals}f}"
        return text.replace(",", "§").replace(".", ",").replace("§", ".")

    @app.errorhandler(404)
    def page_not_found(_error):
        return render_template("errors/404.html", page_title="Página no encontrada"), 404

    @app.errorhandler(500)
    def internal_server_error(_error):
        return render_template("errors/500.html", page_title="Error"), 500

    return app
