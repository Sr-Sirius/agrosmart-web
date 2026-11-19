"""Pruebas de la API del ESP32 y de la página en vivo.

Ejecutar con:  python -m pytest -q
"""

import pytest

from app import create_app
from app.config import Config

CLAVE = "clave-de-prueba"


class ConfigVivo(Config):
    TESTING = True
    ENABLE_DEVICE_API = True
    DEVICE_API_KEY = CLAVE
    DEVICE_RATE_LIMIT = 120
    AGROSMART_DB_CONN = ""


def ciclo(n=1, sustrato2=3250.0, fecha="2026-11-20T10:15:02-05:00", **extra):
    datos = {
        "id_ciclo": n,
        "fecha_hora": fecha,
        "lecturas": [
            {"dispositivo": "DIS-004", "variable": "VAR-001", "valor": 18.4},
            {"dispositivo": "DIS-004", "variable": "VAR-002", "valor": 76.0},
            {"dispositivo": "DIS-001", "variable": "VAR-003", "valor": 3120},
            {"dispositivo": "DIS-002", "variable": "VAR-003", "valor": sustrato2},
            {"dispositivo": "DIS-005", "variable": "VAR-004", "valor": 812.5},
            {"dispositivo": "DIS-003", "variable": "VAR-005", "valor": 3900},
            {"dispositivo": "DIS-003", "variable": "VAR-006", "valor": 1},
        ],
    }
    datos.update(extra)
    return datos


@pytest.fixture()
def client():
    return create_app(ConfigVivo).test_client()


def enviar(client, datos, clave=CLAVE):
    return client.post("/api/lecturas", json=datos, headers={"X-API-Key": clave})


def test_api_desactivada_por_defecto():
    # No depende del .env local: simula la configuración de Render, sin ENABLE_DEVICE_API.
    class ConfigRender(Config):
        TESTING = True
        ENABLE_DEVICE_API = False
    c = create_app(ConfigRender).test_client()
    assert c.post("/api/lecturas", json=ciclo()).status_code == 404
    assert c.get("/monitoreo/en-vivo").status_code == 404


def test_sin_clave_o_clave_invalida(client):
    assert client.post("/api/lecturas", json=ciclo()).status_code == 401
    assert enviar(client, ciclo(), clave="otra").status_code == 401


def test_ciclo_valido(client):
    r = enviar(client, ciclo())
    assert r.status_code == 201
    datos = r.get_json()
    assert datos["aceptadas"] == 7 and datos["rechazadas"] == [] and datos["hora_servidor"] is False
    ultimas = client.get("/api/ultimas").get_json()
    assert ultimas["ultimo"]["id_ciclo"] == 1
    estados = {(l["dispositivo"], l["variable"]): l["estado"] for l in ultimas["ultimo"]["lecturas"]}
    assert estados[("DIS-001", "VAR-003")] == "SECO"
    assert estados[("DIS-003", "VAR-006")] == "SIN_DETECCION"


@pytest.mark.parametrize("datos", [
    {"lecturas": []},
    {"id_ciclo": 0, "lecturas": [{"dispositivo": "DIS-004", "variable": "VAR-001", "valor": 18}]},
    {"id_ciclo": 1},
    [],
])
def test_json_incompleto(client, datos):
    assert enviar(client, datos).status_code == 400


def test_rangos_y_valores_nulos_se_rechazan_con_motivo(client):
    datos = ciclo()
    datos["lecturas"][0]["valor"] = None          # DHT22 sin lectura
    datos["lecturas"][4]["valor"] = -5            # lux negativo
    datos["lecturas"][6]["valor"] = 2             # lluvia digital inválida
    r = enviar(client, datos)
    assert r.status_code == 201
    cuerpo = r.get_json()
    assert cuerpo["aceptadas"] == 4
    motivos = " ".join(x["motivo"] for x in cuerpo["rechazadas"])
    assert "nulo" in motivos and "rango" in motivos


def test_dispositivo_no_registrado(client):
    datos = {"id_ciclo": 3, "lecturas": [{"dispositivo": "DIS-009", "variable": "VAR-001", "valor": 20}]}
    assert enviar(client, datos).status_code == 400


def test_ciclo_duplicado(client):
    assert enviar(client, ciclo(5)).status_code == 201
    assert enviar(client, ciclo(5)).status_code == 409


def test_sin_hora_usa_la_del_servidor(client):
    datos = ciclo(7)
    datos.pop("fecha_hora")
    assert enviar(client, datos).get_json()["hora_servidor"] is True
    datos = ciclo(8, fecha="1970-01-01T00:00:10")
    assert enviar(client, datos).get_json()["hora_servidor"] is True


def test_histeresis_de_la_decision_d1(client):
    # 3.350 → 3.250 → 3.350 → 3.150 → 3.350: la regla anterior cuenta 3 cruces;
    # con histéresis solo hay 2 alertas, porque 3.250 no rearma (no baja de 3.200).
    valores = [3350, 3250, 3350, 3150, 3350]
    for i, v in enumerate(valores, start=1):
        enviar(client, ciclo(i, sustrato2=v, fecha=f"2026-11-20T10:15:{i * 2:02d}-05:00"))
    alertas = client.get("/api/ultimas").get_json()["alertas"]
    assert alertas["sustrato_regla_actual"] == 3
    assert alertas["sustrato_histeresis"] == 2


def test_limite_de_peticiones():
    class Limitada(ConfigVivo):
        DEVICE_RATE_LIMIT = 2

    c = create_app(Limitada).test_client()
    codigos = [enviar(c, ciclo(i, fecha=f"2026-11-20T10:16:{i:02d}-05:00")).status_code for i in range(1, 4)]
    assert codigos == [201, 201, 429]


def test_pagina_en_vivo(client):
    html = client.get("/monitoreo/en-vivo").get_data(as_text=True)
    assert "Monitoreo en vivo" in html and "/api/ultimas" in html
    assert "Ver las lecturas en vivo" in client.get("/monitoreo/").get_data(as_text=True)
