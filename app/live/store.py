"""Almacén en memoria de las últimas lecturas reales (para la página en vivo)."""

import threading
import time
from collections import deque
from datetime import datetime

from app.live.reglas import ZONA_COLOMBIA, Alertas

MAX_CICLOS = 300        # unos 12 minutos a un ciclo cada 2,5 s
MAX_EVENTOS = 50
MAX_RECHAZOS = 20


class Almacen:
    def __init__(self, limite_por_minuto=120):
        self._lock = threading.Lock()
        self.ciclos = deque(maxlen=MAX_CICLOS)
        self.eventos = deque(maxlen=MAX_EVENTOS)
        self.rechazos = deque(maxlen=MAX_RECHAZOS)
        self.recibidos = set()
        self.alertas = Alertas()
        self.limite = limite_por_minuto
        self._peticiones = {}
        self.total_lecturas = 0
        self.ultimo_error_sql = None

    def permitir(self, origen):
        """Límite simple de peticiones por minuto y por dirección IP."""
        ahora = time.monotonic()
        with self._lock:
            cola = self._peticiones.setdefault(origen, deque())
            while cola and ahora - cola[0] > 60:
                cola.popleft()
            if len(cola) >= self.limite:
                return False
            cola.append(ahora)
            return True

    def registrar(self, id_ciclo, fecha, hora_servidor, aceptadas, rechazadas):
        """Guarda el ciclo, aplica las alertas y devuelve los eventos. None si está repetido."""
        clave = (id_ciclo, fecha.isoformat(timespec="seconds"))
        with self._lock:
            if clave in self.recibidos:
                return None
            self.recibidos.add(clave)
            if len(self.recibidos) > 5000:
                self.recibidos = set(list(self.recibidos)[-2500:])
            eventos = []
            for lectura in aceptadas:
                eventos.extend(self.alertas.procesar(lectura, fecha))
            self.ciclos.append({
                "id_ciclo": id_ciclo,
                "fecha_hora": fecha.isoformat(timespec="seconds"),
                "hora_servidor": hora_servidor,
                "recibido": datetime.now(ZONA_COLOMBIA).isoformat(timespec="seconds"),
                "lecturas": aceptadas,
            })
            self.eventos.extend(eventos)
            for rechazo in rechazadas:
                self.rechazos.append(dict(rechazo, id_ciclo=id_ciclo))
            self.total_lecturas += len(aceptadas)
            return eventos

    def resumen(self, n_serie=60):
        with self._lock:
            ciclos = list(self.ciclos)
            serie = {"DIS-001": [], "DIS-002": []}
            for ciclo in ciclos[-n_serie:]:
                for lectura in ciclo["lecturas"]:
                    if lectura["variable"] == "VAR-003":
                        serie[lectura["dispositivo"]].append(lectura["valor"])
            return {
                "ultimo": ciclos[-1] if ciclos else None,
                "ciclos_en_memoria": len(ciclos),
                "total_lecturas": self.total_lecturas,
                "serie_sustrato": serie,
                "alertas": dict(self.alertas.conteo),
                "alerta_activa": dict(self.alertas.activa),
                "eventos": list(self.eventos)[-10:][::-1],
                "rechazos": list(self.rechazos)[-5:][::-1],
                "ultimo_error_sql": self.ultimo_error_sql,
            }
