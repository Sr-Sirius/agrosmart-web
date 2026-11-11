from flask import Blueprint, render_template

project_bp = Blueprint("project", __name__)


@project_bp.get("/")
def overview():
    return render_template("proyecto.html", page_title="El proyecto")
