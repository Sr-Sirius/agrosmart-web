from flask import Blueprint, render_template

monitoring_bp = Blueprint("monitoring", __name__)


@monitoring_bp.get("/")
def dashboard():
    # La recepción en vivo desde el ESP32 se integrará en una fase posterior.
    # Mientras tanto, la página resume el periodo simulado cargado en AgroSmart DW.
    return render_template("monitoreo.html", page_title="Monitoreo")
