"""Catálogo, validación y reglas de alerta para las lecturas reales del ESP32.

Los códigos, rangos y clasificaciones son los mismos de AgroSmartDB y de la
simulación (tabla VARIABLE y script de generación de mediciones).
"""

from datetime import datetime, timedelta, timezone

ZONA_COLOMBIA = timezone(timedelta(hours=-5), name="UTC-05:00")

# (dispositivo, variable) -> proceso al que pertenece la medición en PROCESO_DISPOSITIVO
CATALOGO = {
    ("DIS-001", "VAR-003"): "PRO-002",
    ("DIS-002", "VAR-003"): "PRO-002",
    ("DIS-004", "VAR-001"): "PRO-001",
    ("DIS-004", "VAR-002"): "PRO-001",
    ("DIS-005", "VAR-004"): "PRO-001",
    ("DIS-003", "VAR-005"): "PRO-001",
    ("DIS-003", "VAR-006"): "PRO-001",
}

# Rangos de la tabla VARIABLE de AgroSmartDB
RANGOS = {
    "VAR-001": (-40.0, 80.0),
    "VAR-002": (0.0, 100.0),
    "VAR-003": (0.0, 4095.0),
    "VAR-004": (0.0, 65535.0),
    "VAR-005": (0.0, 4095.0),
    "VAR-006": (0.0, 1.0),
}

UMBRAL_SUSTRATO = 3300.0          # alerta de sustrato muy seco (ADC)
REARME_SUSTRATO = 3200.0          # decisión D1: la alerta se rearma por debajo de este valor
UMBRAL_TEMPERATURA = 25.0         # °C
UMBRAL_ILUMINACION = 150.0        # lux, solo entre las 7 y las 17 h


def clasificar(variable, valor, lluvia_detectada=False):
    """Devuelve estado_clasificacion con las mismas reglas de la simulación."""
    if variable == "VAR-003":
        if valor < 2500:
            return "MOJADO"
        if valor <= 2600:
            return "HUMEDO"
        if valor < 2800:
            return "HUMEDAD INTERMEDIA"
        return "SECO"
    if variable == "VAR-001":
        return "ALERTA" if valor >= UMBRAL_TEMPERATURA else "NORMAL"
    if variable == "VAR-002":
        if valor >= 80:
            return "ALTA"
        return "MEDIA" if valor >= 60 else "BAJA"
    if variable == "VAR-004":
        if valor < 100:
            return "BAJA"
        return "MEDIA" if valor < 500 else "ALTA"
    if variable == "VAR-005":
        return "HUMEDO" if lluvia_detectada else "SECO"
    if variable == "VAR-006":
        return "LLUVIA_DETECTADA" if valor == 0 else "SIN_DETECCION"
    return None


def leer_fecha(texto):
    """Convierte la fecha ISO del ESP32 a hora de Colombia. Devuelve None si no es válida."""
    if not isinstance(texto, str) or not texto:
        return None
    try:
        fecha = datetime.fromisoformat(texto)
    except ValueError:
        return None
    if fecha.tzinfo is None:
        fecha = fecha.replace(tzinfo=ZONA_COLOMBIA)
    fecha = fecha.astimezone(ZONA_COLOMBIA)
    # Un ESP32 sin NTP reporta fechas de 1970; esas lecturas usan la hora del servidor.
    if fecha.year < 2026:
        return None
    return fecha


def validar_ciclo(datos):
    """Valida el JSON de un ciclo.

    Devuelve (error_general, aceptadas, rechazadas). Si hay error_general, el ciclo completo
    se rechaza con 400. Las lecturas individuales inválidas se rechazan con su motivo, como en
    etl.REGISTRO_RECHAZADO, y las válidas se aceptan.
    """
    if not isinstance(datos, dict):
        return "El cuerpo debe ser un objeto JSON.", [], []
    id_ciclo = datos.get("id_ciclo")
    if not isinstance(id_ciclo, int) or isinstance(id_ciclo, bool) or id_ciclo <= 0:
        return "id_ciclo debe ser un entero mayor que 0.", [], []
    lecturas = datos.get("lecturas")
    if not isinstance(lecturas, list) or not lecturas:
        return "lecturas debe ser una lista con al menos una lectura.", [], []
    if len(lecturas) > len(CATALOGO):
        return f"Un ciclo admite como máximo {len(CATALOGO)} lecturas.", [], []

    aceptadas, rechazadas, vistas = [], [], set()
    for lectura in lecturas:
        if not isinstance(lectura, dict):
            rechazadas.append({"lectura": lectura, "motivo": "La lectura no es un objeto."})
            continue
        dispositivo = lectura.get("dispositivo")
        variable = lectura.get("variable")
        valor = lectura.get("valor")
        clave = (dispositivo, variable)
        if clave not in CATALOGO:
            motivo = "Combinación de dispositivo y variable no registrada."
        elif clave in vistas:
            motivo = "Lectura repetida dentro del mismo ciclo."
        elif valor is None:
            motivo = "Valor nulo (fallo de lectura del sensor)."
        elif isinstance(valor, bool) or not isinstance(valor, (int, float)):
            motivo = "El valor no es numérico."
        elif not RANGOS[variable][0] <= valor <= RANGOS[variable][1]:
            motivo = "Valor fuera del rango {}–{}.".format(*RANGOS[variable])
        elif variable == "VAR-006" and valor not in (0, 1):
            motivo = "La lluvia digital solo admite 0 o 1."
        else:
            motivo = None
        if motivo:
            rechazadas.append({"dispositivo": dispositivo, "variable": variable, "valor": valor,
                               "motivo": motivo})
        else:
            vistas.add(clave)
            aceptadas.append({"dispositivo": dispositivo, "variable": variable, "valor": float(valor),
                              "proceso": CATALOGO[clave]})

    lluvia = any(l["variable"] == "VAR-006" and l["valor"] == 0 for l in aceptadas)
    for lectura in aceptadas:
        lectura["estado"] = clasificar(lectura["variable"], lectura["valor"], lluvia)
    return None, aceptadas, rechazadas


class Alertas:
    """Aplica las reglas de alerta a las lecturas en orden de llegada.

    Para el sustrato cuenta las dos reglas en paralelo: la actual (cruce de 3.300 ADC) y la
    de la decisión D1 (activa en 3.300, se rearma por debajo de 3.200). Así la página en vivo
    muestra cuántas alertas se evitan con la histéresis.
    """

    def __init__(self):
        self.anterior = {}            # (dispositivo, variable) -> último valor
        self.activa = {"DIS-001": False, "DIS-002": False}
        self.conteo = {
            "sustrato_regla_actual": 0,
            "sustrato_histeresis": 0,
            "temperatura": 0,
            "iluminacion": 0,
        }

    def procesar(self, lectura, fecha):
        """Devuelve la lista de eventos que genera la lectura (puede ser vacía)."""
        dispositivo, variable, valor = lectura["dispositivo"], lectura["variable"], lectura["valor"]
        previo = self.anterior.get((dispositivo, variable))
        self.anterior[(dispositivo, variable)] = valor
        eventos = []

        def evento(tipo, regla):
            return {"tipo": tipo, "regla": regla, "dispositivo": dispositivo, "valor": valor,
                    "fecha_hora": fecha.isoformat(timespec="seconds")}

        if variable == "VAR-003":
            if valor >= UMBRAL_SUSTRATO and (previo is None or previo < UMBRAL_SUSTRATO):
                self.conteo["sustrato_regla_actual"] += 1
            if not self.activa[dispositivo] and valor >= UMBRAL_SUSTRATO:
                self.activa[dispositivo] = True
                self.conteo["sustrato_histeresis"] += 1
                eventos.append(evento("ALERTA_HUMEDAD_SUSTRATO", "histéresis 3.300/3.200 (D1)"))
            elif self.activa[dispositivo] and valor < REARME_SUSTRATO:
                self.activa[dispositivo] = False
        elif variable == "VAR-001":
            if valor >= UMBRAL_TEMPERATURA and (previo is None or previo < UMBRAL_TEMPERATURA):
                self.conteo["temperatura"] += 1
                eventos.append(evento("ALERTA_TEMPERATURA", "cruce de 25 °C"))
        elif variable == "VAR-004" and 7 <= fecha.hour <= 17:
            if valor < UMBRAL_ILUMINACION and (previo is None or previo >= UMBRAL_ILUMINACION):
                self.conteo["iluminacion"] += 1
                eventos.append(evento("ALERTA_ILUMINACION", "menos de 150 lux entre 7 y 17 h"))
        return eventos
