"""Simula el ESP32 enviando ciclos a la API local. Sirve para probar sin el hardware.

Uso (PowerShell, con la API corriendo):
    python tools/simulador_esp32.py --url http://127.0.0.1:5000/api/lecturas --clave TU_CLAVE
Opciones: --ciclos 0 (infinito), --intervalo 2.5, --sin-hora (prueba la hora del servidor)
"""

import argparse
import math
import random
import time
from datetime import datetime, timedelta, timezone

import requests

ZONA = timezone(timedelta(hours=-5))


def ciclo(n, con_hora=True):
    ahora = datetime.now(ZONA)
    h = ahora.hour + ahora.minute / 60
    lluvia = random.random() < 0.05
    sol = max(0.0, math.sin(math.pi * (h - 6) / 12)) if 6 <= h <= 18 else 0.0
    datos = {
        "id_ciclo": n,
        "lecturas": [
            {"dispositivo": "DIS-004", "variable": "VAR-001",
             "valor": round(17.5 + 5.5 * math.sin(2 * math.pi * (h - 10) / 24) + random.uniform(-0.4, 0.4), 2)},
            {"dispositivo": "DIS-004", "variable": "VAR-002", "valor": round(random.uniform(66, 84), 2)},
            {"dispositivo": "DIS-001", "variable": "VAR-003", "valor": round(3150 + random.uniform(-100, 100), 1)},
            # La Parcela 2 oscila alrededor de 3.300 para mostrar el efecto de la histéresis.
            {"dispositivo": "DIS-002", "variable": "VAR-003", "valor": round(3280 + random.uniform(-100, 100), 1)},
            {"dispositivo": "DIS-005", "variable": "VAR-004",
             "valor": round(sol * (900 + random.uniform(-60, 60)) * (0.18 if lluvia else 1), 2)},
            {"dispositivo": "DIS-003", "variable": "VAR-005", "valor": random.randint(1900, 2300) if lluvia else random.randint(3900, 4095)},
            {"dispositivo": "DIS-003", "variable": "VAR-006", "valor": 0 if lluvia else 1},
        ],
    }
    if con_hora:
        datos["fecha_hora"] = ahora.isoformat(timespec="seconds")
    return datos


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--url", default="http://127.0.0.1:5000/api/lecturas")
    p.add_argument("--clave", required=True)
    p.add_argument("--ciclos", type=int, default=0)
    p.add_argument("--intervalo", type=float, default=2.5)
    p.add_argument("--sin-hora", action="store_true")
    a = p.parse_args()

    n = 1
    while a.ciclos == 0 or n <= a.ciclos:
        try:
            r = requests.post(a.url, json=ciclo(n, not a.sin_hora), headers={"X-API-Key": a.clave}, timeout=5)
            print(n, r.status_code, r.json())
        except requests.RequestException as exc:
            print(n, "sin conexión:", exc)
        n += 1
        time.sleep(a.intervalo)


if __name__ == "__main__":
    main()
