from flask import Blueprint, render_template

monitoring_bp = Blueprint("monitoring", __name__)


@monitoring_bp.get("/")
def dashboard():
    # Placeholder: the live ESP32/API and SQL Server integration will be added later.
    return render_template("monitoreo.html", page_title="Monitoreo")
