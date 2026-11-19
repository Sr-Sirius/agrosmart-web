"""API del ESP32 y página de monitoreo en vivo.

Solo se registra si ENABLE_DEVICE_API=1 (equipo BELLATOR en la red local).
En Render la variable no existe y el sitio público no cambia.
"""

import hmac
from datetime import datetime

from flask import Blueprint, current_app, jsonify, render_template, request

from app.live.reglas import ZONA_COLOMBIA, leer_fecha, validar_ciclo
from app.live.store import Almacen

live_bp = Blueprint("live", __name__)


def almacen():
    return current_app.extensions["agrosmart_live"]


@live_bp.post("/api/lecturas")
def recibir_lecturas():
    clave = current_app.config.get("DEVICE_API_KEY", "")
    if not clave:
        return jsonify(error="La API no tiene clave configurada (DEVICE_API_KEY)."), 503
    enviada = request.headers.get("X-API-Key", "")
    if not hmac.compare_digest(enviada.encode(), clave.encode()):
        return jsonify(error="Falta el encabezado X-API-Key o la clave no es válida."), 401
    if not almacen().permitir(request.remote_addr or "desconocido"):
        return jsonify(error="Demasiadas peticiones; espera un minuto."), 429

    datos = request.get_json(silent=True)
    error, aceptadas, rechazadas = validar_ciclo(datos)
    if error:
        return jsonify(error=error), 400
    if not aceptadas:
        return jsonify(error="Ninguna lectura es válida.", rechazadas=rechazadas), 400

    fecha = leer_fecha(datos.get("fecha_hora"))
    hora_servidor = fecha is None
    if hora_servidor:
        fecha = datetime.now(ZONA_COLOMBIA)

    eventos = almacen().registrar(datos["id_ciclo"], fecha, hora_servidor, aceptadas, rechazadas)
    if eventos is None:
        return jsonify(error="Ciclo repetido: ya se recibió ese id_ciclo con esa fecha."), 409

    respuesta = {"aceptadas": len(aceptadas), "rechazadas": rechazadas, "eventos": eventos,
                 "hora_servidor": hora_servidor, "guardado_sql": False}
    cadena = current_app.config.get("AGROSMART_DB_CONN", "")
    if cadena:
        from app.live.sqlserver import guardar_ciclo
        try:
            respuesta["id_ciclo_captura"] = guardar_ciclo(cadena, fecha, aceptadas)
            respuesta["guardado_sql"] = True
            almacen().ultimo_error_sql = None
        except Exception as exc:  # la lectura queda en memoria aunque falle SQL Server
            current_app.logger.warning("No se pudo guardar en AgroSmartDB: %s", exc)
            almacen().ultimo_error_sql = type(exc).__name__
    return jsonify(respuesta), 201


@live_bp.get("/api/ultimas")
def ultimas():
    datos = almacen().resumen()
    datos["sql_activo"] = bool(current_app.config.get("AGROSMART_DB_CONN"))
    return jsonify(datos)


@live_bp.get("/monitoreo/en-vivo")
def en_vivo():
    return render_template("monitoreo_vivo.html", page_title="Monitoreo en vivo")


def registrar(app):
    app.extensions["agrosmart_live"] = Almacen(app.config.get("DEVICE_RATE_LIMIT", 120))
    app.register_blueprint(live_bp)
