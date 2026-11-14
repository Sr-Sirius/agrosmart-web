from flask import Blueprint, render_template

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.get("/")
def dashboard():
    # La URL de inserción de Power BI se lee de la variable de entorno POWERBI_EMBED_URL.
    return render_template("analitica/dashboard.html", page_title="Dashboard de Power BI")


@analytics_bp.get("/preparacion")
def preparation():
    return render_template("analitica/preparacion.html", page_title="Preparación del análisis")


@analytics_bp.get("/conocimientos")
def knowledge():
    return render_template("analitica/conocimientos.html", page_title="Conocimientos evidentes")


@analytics_bp.get("/validacion-decisiones")
def decisions():
    return render_template("analitica/decisiones.html", page_title="Validación y decisiones")
