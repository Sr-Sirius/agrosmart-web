from flask import Blueprint, render_template

project_bp = Blueprint("project", __name__)


@project_bp.get("/")
def overview():
    return render_template("proyecto/identificacion.html", page_title="Identificación, problema y objetivos")


@project_bp.get("/marco-referencial")
def framework():
    return render_template("proyecto/marco.html", page_title="Marco referencial")


@project_bp.get("/metodologia")
def methodology():
    return render_template("proyecto/metodologia.html", page_title="Metodología y cronograma")


@project_bp.get("/solucion")
def solution():
    return render_template("proyecto/solucion.html", page_title="Desarrollo de la solución")


@project_bp.get("/datos")
def data():
    return render_template("proyecto/datos.html", page_title="Gestión de los datos")
