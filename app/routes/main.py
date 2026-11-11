from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def home():
    return render_template("index.html", page_title="Inicio")


@main_bp.get("/acerca")
def about():
    return render_template("acerca.html", page_title="Acerca de")
