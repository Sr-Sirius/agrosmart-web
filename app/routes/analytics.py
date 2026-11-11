from flask import Blueprint, current_app, render_template

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.get("/")
def dashboard():
    # The Power BI embed URL is configured later through an environment variable.
    return render_template(
        "analitica.html",
        page_title="Analítica",
        powerbi_embed_url=current_app.config.get("POWERBI_EMBED_URL", ""),
    )
