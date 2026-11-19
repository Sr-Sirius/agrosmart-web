"""Escritura opcional de las lecturas reales en AgroSmartDB (SQL Server, red local).

Solo se usa si la variable de entorno AGROSMART_DB_CONN tiene una cadena ODBC, por ejemplo:
    DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=AgroSmartDB;
    Trusted_Connection=yes;TrustServerCertificate=yes
La cadena va en el archivo .env (excluido de Git), nunca en el código.
"""

SQL_SIGUIENTE_CICLO = (
    "SELECT ISNULL(MAX(id_ciclo_captura), 0) + 1 FROM dbo.MEDICION WITH (UPDLOCK, HOLDLOCK)"
)

SQL_INSERTAR = """
INSERT INTO dbo.MEDICION
    (id_ciclo_captura, id_dispositivo, id_variable, id_proceso,
     fecha_hora, valor, estado_clasificacion, origen_dato)
SELECT ?, d.id_dispositivo, v.id_variable, p.id_proceso, ?, ?, ?, 'REAL'
FROM dbo.DISPOSITIVO d
JOIN dbo.VARIABLE v ON v.codigo_variable = ?
JOIN dbo.PROCESO  p ON p.codigo_proceso  = ?
WHERE d.codigo_dispositivo = ?
"""


def guardar_ciclo(cadena, fecha, lecturas):
    """Inserta las lecturas de un ciclo en dbo.MEDICION con origen REAL.

    El id_ciclo_captura lo asigna el servidor (máximo actual + 1) para no chocar con los
    ciclos simulados ni con los reinicios del ESP32. Devuelve el id asignado.
    """
    import pyodbc  # solo se necesita en BELLATOR (requirements-local.txt)

    fecha_local = fecha.replace(tzinfo=None, microsecond=0)
    conexion = pyodbc.connect(cadena, autocommit=False, timeout=5)
    try:
        cursor = conexion.cursor()
        id_ciclo = cursor.execute(SQL_SIGUIENTE_CICLO).fetchone()[0]
        for l in lecturas:
            cursor.execute(SQL_INSERTAR, id_ciclo, fecha_local, l["valor"], l["estado"],
                           l["variable"], l["proceso"], l["dispositivo"])
            if cursor.rowcount != 1:
                raise RuntimeError(f"No se encontró {l['dispositivo']}/{l['variable']} en AgroSmartDB.")
        conexion.commit()
        return int(id_ciclo)
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
