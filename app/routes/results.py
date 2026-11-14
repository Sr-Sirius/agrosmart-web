from flask import Blueprint, render_template

results_bp = Blueprint("results", __name__)


@results_bp.get("/")
def products():
    return render_template("resultados/productos.html", page_title="Productos y resultados")


@results_bp.get("/conclusiones")
def conclusions():
    return render_template("resultados/conclusiones.html", page_title="Conclusiones y referencias")
