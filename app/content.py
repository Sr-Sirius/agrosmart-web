"""Contenido del sitio de AgroSmart.

Todos los textos y cifras del sitio están centralizados en este archivo para que
el equipo pueda corregirlos sin modificar las plantillas.

Las cifras provienen del Data Warehouse AgroSmart DW, del dashboard de Power BI
y de las consultas de validación en SQL Server (periodo simulado del 01/11/2026
00:00:00 al 04/11/2026 07:21:50). No se deben cambiar sin volver a calcularlas.
"""

# ---------------------------------------------------------------------------
# Identificación del PGC
# ---------------------------------------------------------------------------
IDENTIFICACION = {
    "titulo": "AgroSmart: monitoreo IoT y analítica de datos para el módulo agropecuario "
              "de la ciudad inteligente NEOGRID",
    "programa": "Ingeniería de Sistemas y Computación",
    "institucion": "Universidad de Cundinamarca",
    "sede": "Extensión Chía",
    "ciclo": "Ciclo III: Investigación-Producción (VII semestre)",
    "tipo": "Proyecto Tecnológico",
    "integrantes": ["Michael Steeven Sanchez", "Juan David Rodríguez Devia"],
    "gestor": "Edison Gustavo Cañón Varela",
    "nucleo": "Big Data",
    "periodo": "2026-II",
    "linea": "Aprendizaje, conocimiento, tecnologías, comunicación y digitalización",
    "productos": ["Prototipo", "Sistema de información", "Desarrollo web",
                  "Documento síntesis del PGC", "Producción de contenidos digitales"],
}

ENLACES = {
    "repositorio": "https://github.com/Sr-Sirius/agrosmart-web",
    "sitio": "https://agrosmart-web-b0bl.onrender.com",
}

PERIODO = "01/11/2026 00:00:00 – 04/11/2026 07:21:50"
PERIODO_CORTO = "01–04/11/2026"

# ---------------------------------------------------------------------------
# NEOGRID
# ---------------------------------------------------------------------------
NEOGRID_COMPONENTES = [
    {"nombre": "Agro (AgroSmart)", "detalle": "Tablero de 35 × 50 cm. Monitoreo ambiental, del sustrato y control de compuerta.", "actual": True},
    {"nombre": "Energía solar", "detalle": "Tablero de 35 × 50 cm con seguidor solar y central.", "actual": False},
    {"nombre": "Contaminación acústica", "detalle": "Tablero de 35 × 50 cm.", "actual": False},
    {"nombre": "Tuberías y aguas residuales", "detalle": "Tablero de 35 × 50 cm.", "actual": False},
    {"nombre": "Alumbrado público", "detalle": "Dos tableros de 15 × 100 cm (oeste y este).", "actual": False},
    {"nombre": "Tráfico", "detalle": "Tablero central de 20 × 100 cm con la avenida principal.", "actual": False},
]

# ---------------------------------------------------------------------------
# Indicadores generales (sin filtros)
# ---------------------------------------------------------------------------
INDICADORES = [
    {"nombre": "Mediciones", "valor": "999.992", "unidad": "lecturas",
     "calculo": "Suma de cantidad_mediciones.", "denominador": None},
    {"nombre": "Eventos", "valor": "25.581", "unidad": "eventos",
     "calculo": "Suma de cantidad_eventos.", "denominador": None},
    {"nombre": "Alertas", "valor": "25.146", "unidad": "alertas",
     "calculo": "Eventos de tipo ALERTA_HUMEDAD_SUSTRATO, ALERTA_TEMPERATURA y ALERTA_ILUMINACION.", "denominador": None},
    {"nombre": "% de alertas sobre eventos", "valor": "98,30 %", "unidad": "",
     "calculo": "Alertas ÷ eventos.", "denominador": "Total de eventos del periodo (25.581)."},
    {"nombre": "Alertas por 1.000 mediciones", "valor": "25,15", "unidad": "",
     "calculo": "Alertas ÷ mediciones × 1.000.", "denominador": "Total de mediciones del periodo (999.992)."},
    {"nombre": "Dispositivos activos", "valor": "5 de 7", "unidad": "",
     "calculo": "Dispositivos distintos con al menos una medición.", "denominador": "Siete dispositivos registrados; el SG90 y el ESP32 no generan mediciones."},
    {"nombre": "% de lecturas con lluvia", "valor": "11,34 %", "unidad": "",
     "calculo": "Lecturas de VAR-006 con valor 0 ÷ lecturas de VAR-006.", "denominador": "Lecturas de lluvia digital (142.856); 16.200 detectaron agua."},
    {"nombre": "Temperatura promedio", "valor": "17,07", "unidad": "°C",
     "calculo": "Promedio de VAR-001 (mediana 16,75 °C).", "denominador": None},
]

# ---------------------------------------------------------------------------
# Preguntas orientadoras
# ---------------------------------------------------------------------------
PREGUNTAS = [
    {"id": "P1", "texto": "¿Cuál es el volumen de mediciones, eventos y alertas del periodo, y qué proporción de los eventos corresponde a alertas?", "analisis": "Indicadores generales"},
    {"id": "P2", "texto": "¿Cómo se distribuye la temperatura y qué tan cerca está del umbral de alerta de 25 °C?", "analisis": "U1"},
    {"id": "P3", "texto": "¿Qué tipos de evento predominan en el módulo?", "analisis": "U2"},
    {"id": "P4", "texto": "¿En qué estado se encuentra el sustrato durante la mayor parte del tiempo?", "analisis": "U3"},
    {"id": "P5", "texto": "¿Cómo varían la temperatura y la humedad relativa a lo largo del día y cómo se relacionan entre sí?", "analisis": "B1"},
    {"id": "P6", "texto": "¿Difiere la humedad del sustrato entre los dos sensores, es decir, entre las dos parcelas?", "analisis": "B2"},
    {"id": "P7", "texto": "¿Cómo cambia la iluminación diurna cuando se detecta lluvia?", "analisis": "B3"},
    {"id": "P8", "texto": "¿En qué ubicación, franja del día y tipo de dispositivo se concentran las alertas?", "analisis": "M1"},
]

# ---------------------------------------------------------------------------
# Datos para las visualizaciones (valores verificados)
# ---------------------------------------------------------------------------
EVENTOS_POR_TIPO = [
    {"label": "ALERTA_HUMEDAD_SUSTRATO", "valor": 24339, "pct": "95,14 %", "detalle": "DIS-001 Parcela 1: 5.873 · DIS-002 Parcela 2: 18.466"},
    {"label": "ALERTA_ILUMINACION", "valor": 807, "pct": "3,15 %", "detalle": "DIS-005, Acceso del invernadero"},
    {"label": "PUERTA_ABIERTA", "valor": 263, "pct": "1,03 %", "detalle": "DIS-006, Acceso del invernadero"},
    {"label": "PUERTA_CERRADA", "valor": 169, "pct": "0,66 %", "detalle": "DIS-006, Acceso del invernadero"},
    {"label": "LLUVIA_DETECTADA", "valor": 3, "pct": "0,01 %", "detalle": "DIS-003, Ambiente general"},
    {"label": "ALERTA_TEMPERATURA", "valor": 0, "pct": "0 %", "detalle": "Ninguna lectura alcanzó 25 °C"},
]

EVENTOS_POR_DIA = [
    {"label": "01/11", "valor": 7800},
    {"label": "02/11", "valor": 9174},
    {"label": "03/11", "valor": 8234},
    {"label": "04/11*", "valor": 373},
]

TEMP_ESTADISTICOS = [
    {"label": "Mínima", "valor": 9.53},
    {"label": "Percentil 1", "valor": 10.74},
    {"label": "Mediana", "valor": 16.75},
    {"label": "Media", "valor": 17.07},
    {"label": "Percentil 99", "valor": 23.98},
    {"label": "Máxima", "valor": 24.50},
]

TEMP_FRANJA = [
    {"label": "Madrugada (0–5 h)", "valor": 13.01},
    {"label": "Mañana (6–11 h)", "valor": 16.02},
    {"label": "Tarde (12–17 h)", "valor": 21.89},
    {"label": "Noche (18–23 h)", "valor": 18.78},
]

SUSTRATO_ESTADO = [
    {"label": "SECO (≥ 2.800 ADC)", "valor": 273366, "pct": "95,68 %"},
    {"label": "HUMEDAD_INTERMEDIA (2.600–2.800)", "valor": 12270, "pct": "4,29 %"},
    {"label": "HÚMEDO (2.500–2.600)", "valor": 76, "pct": "0,03 %"},
    {"label": "MOJADO (< 2.500)", "valor": 0, "pct": "0 %"},
]

SUSTRATO_SENSORES = {
    "grupos": ["Sensor 1 · Parcela 1", "Sensor 2 · Parcela 2"],
    "series": [
        {"nombre": "Promedio", "valores": [3098.81, 3217.41]},
        {"nombre": "Mediana", "valores": [3127.87, 3241.45]},
    ],
}

SUSTRATO_TABLA = [
    ["Media (ADC)", "3.098,81", "3.217,41"],
    ["Mediana (ADC)", "3.127,87", "3.241,45"],
    ["Desviación estándar (ADC)", "154,24", "131,50"],
    ["Lecturas ≥ 3.300 ADC", "4,67 % (6.671)", "25,82 % (36.879)"],
    ["Lecturas ≥ 3.300 ADC de noche", "18,3 %", "64,6 %"],
    ["Lecturas por sensor", "142.856", "142.856"],
]

SUSTRATO_UMBRAL = {
    "grupos": ["Todo el periodo", "Franja noche|(18–23 h)"],
    "series": [
        {"nombre": "Sensor 1 · Parcela 1", "valores": [4.67, 18.3]},
        {"nombre": "Sensor 2 · Parcela 2", "valores": [25.82, 64.6]},
    ],
}

ILUMINACION_LLUVIA = {
    "grupos": ["Promedio 6–17 h", "Mediana 6–17 h", "Promedio 12–17 h|(control de hora)"],
    "series": [
        {"nombre": "Sin lluvia", "valores": [802.69, 842.47, 828.22]},
        {"nombre": "Con lluvia", "valores": [148.62, 156.56, 148.62]},
    ],
}

ILUMINACION_TABLA = [
    ["Promedio 6–17 h (lux)", "802,69 (n = 56.456)", "148,62 (n = 10.800)", "−81,5 %"],
    ["Mediana 6–17 h (lux)", "842,47", "156,56", ""],
    ["Promedio 12–17 h, control de hora (lux)", "828,22 (n = 21.600)", "148,62", "−82,1 %"],
    ["Lecturas < 150 lux entre 7 y 17 h", "3,3 %", "47,0 %", ""],
]

B1_EXTREMOS = [
    ["Temperatura promedio por hora", "12,14 °C a las 2 h", "22,56 °C a las 15 h"],
    ["Humedad relativa promedio por hora", "68,42 % a las 18 h", "84,10 % a las 2 h"],
]

MATRIZ = {
    "columnas": ["Madrugada", "Mañana", "Tarde", "Noche", "Total"],
    "filas": [
        {"ubicacion": "Acceso del invernadero", "tipo": "SENSOR",
         "celdas": [(0, "0,00"), (0, "0,00"), (807, "24,91"), (0, "0,00"), (807, "5,65")]},
        {"ubicacion": "Parcela 1", "tipo": "SENSOR",
         "celdas": [(0, "0,00"), (0, "0,00"), (693, "21,39"), (5180, "159,88"), (5873, "41,11")]},
        {"ubicacion": "Parcela 2", "tipo": "SENSOR",
         "celdas": [(5249, "121,50"), (325, "9,32"), (4916, "151,73"), (7976, "246,17"), (18466, "129,26")]},
    ],
    "total": [(5249, "17,36"), (325, "1,33"), (6416, "28,29"), (13156, "58,01"), (25146, "25,15")],
    "tamanos": "Mediciones por sensor y franja: madrugada 43.200; mañana 34.856; tarde 32.400; noche 32.400.",
}

REGLAS_ALERTA = {
    "grupos": ["Actual:|cruce de 3.300", "Histéresis|3.300/3.250", "Histéresis|3.300/3.200", "Persistencia de|3 lecturas"],
    "series": [
        {"nombre": "Sensor 1 · Parcela 1", "valores": [5873, 5461, 4636, 80]},
        {"nombre": "Sensor 2 · Parcela 2", "valores": [18466, 11379, 4678, 4147]},
    ],
}

REGLAS_TABLA = [
    ["Actual (cruce de 3.300)", "5.873", "18.466", "24.339", "—"],
    ["Histéresis 3.300/3.250", "5.461", "11.379", "16.840", "−30,8 %"],
    ["Histéresis 3.300/3.200", "4.636", "4.678", "9.314", "−61,7 %"],
    ["Persistencia de 3 lecturas ≥ 3.300", "80", "4.147", "4.227", "−82,6 %"],
]

# ---------------------------------------------------------------------------
# Conocimientos evidentes
# ---------------------------------------------------------------------------
CONOCIMIENTOS = [
    {
        "id": "C1",
        "titulo": "La temperatura es bimodal y nunca alcanza el umbral de alerta",
        "analisis": "U1 · Análisis univariado",
        "pagina": "Análisis univariados",
        "pregunta": "¿Cómo se distribuye la temperatura y qué tan cerca está del umbral de 25 °C que activa ALERTA_TEMPERATURA? La pregunta permite saber si el monitoreo térmico del módulo está detectando condiciones de riesgo.",
        "variables": "VAR-001 Temperatura (°C) del DHT22; franja_dia de DIM_HORA. n = 142.856 lecturas.",
        "procedimiento": "Se filtró codigo_concepto = VAR-001, se agruparon las lecturas en rangos de 1 °C con el grupo «valor (rangos de 1)» y se calcularon media, mediana, mínima, máxima y percentiles. Luego se promedió la temperatura por franja del día.",
        "resultado": "Media 17,07 °C, mediana 16,75 °C, desviación estándar 3,88 °C, mínima 9,53 °C y máxima 24,50 °C. Solo 1.357 lecturas (0,95 %) superan 24 °C y ninguna llega a 25 °C. El histograma tiene dos picos: 13 °C (14.746 lecturas) y 21 °C (13.240), con un valle en 17 °C (7.979). Por franja: madrugada 13,01; mañana 16,02; tarde 21,89; noche 18,78 °C.",
        "hallazgo": "La distribución es bimodal: un modo corresponde a las horas frías de la noche y la madrugada, y otro a la tarde. La máxima queda 0,5 °C por debajo del umbral, por eso hay 0 alertas de temperatura.",
        "interpretacion": "La media de 17,07 °C cae en el valle del histograma, es decir, en un valor poco frecuente; no describe una condición típica del invernadero. Para este módulo es más útil describir la temperatura por franja que con un único promedio.",
        "utilidad": "Indica que el umbral de 25 °C no se activó en el escenario y que las acciones térmicas deben planearse por franja horaria (la tarde es la más cálida).",
        "limitacion": "Son 3,3 días simulados con un solo sensor ambiental. La ausencia de alertas no demuestra que el umbral sea adecuado para un cultivo real.",
        "grafico": "c1",
    },
    {
        "id": "C2",
        "titulo": "Las alertas de humedad del sustrato dominan los eventos",
        "analisis": "U2 · Análisis univariado",
        "pagina": "Análisis univariados",
        "pregunta": "¿Qué tipos de evento predominan? La respuesta muestra a qué proceso debe dedicar más atención el operador y si las alertas son selectivas.",
        "variables": "codigo_concepto de DIM_CONCEPTO (tipo_concepto = EVENTO), cantidad_eventos, dispositivo y ubicación.",
        "procedimiento": "Se filtraron los conceptos de tipo EVENTO, se sumó cantidad_eventos por codigo_concepto y se calculó el porcentaje sobre el total de eventos (25.581). La tasa por hora se obtuvo dividiendo entre las 79,4 horas del periodo.",
        "resultado": "ALERTA_HUMEDAD_SUSTRATO: 24.339 eventos (95,14 %). ALERTA_ILUMINACION: 807 (3,15 %). PUERTA_ABIERTA: 263 (1,03 %). PUERTA_CERRADA: 169 (0,66 %). LLUVIA_DETECTADA: 3 (0,01 %). ALERTA_TEMPERATURA: 0. Las alertas de sustrato equivalen a unas 307 por hora.",
        "hallazgo": "Casi todos los eventos son alertas del sustrato, generadas por los dos sensores capacitivos. La validación mostró que son cruces repetidos del umbral de 3.300 ADC dentro de un mismo episodio: el ruido de ±100 ADC hace que la lectura oscile alrededor del límite.",
        "interpretacion": "Más de 300 alertas por hora no se pueden atender una por una. Esto produce fatiga de alertas: las notificaciones importantes se pierden entre repeticiones.",
        "utilidad": "Sustenta la decisión D1: rediseñar la regla de alerta del sustrato antes de usarla para operar el riego.",
        "limitacion": "No hay registro del tiempo de atención de las alertas, así que no se puede medir su efecto real sobre el operador.",
        "grafico": "c2",
    },
    {
        "id": "C3",
        "titulo": "La temperatura y la humedad relativa se mueven en sentido inverso",
        "analisis": "B1 · Análisis bivariado",
        "pagina": "Análisis bivariados",
        "pregunta": "¿Cómo varían la temperatura y la humedad relativa a lo largo del día y cómo se relacionan? Sirve para identificar las horas de mayor exigencia ambiental.",
        "variables": "VAR-001 Temperatura (°C) y VAR-002 Humedad relativa (%) del DHT22; hora de DIM_HORA.",
        "procedimiento": "Se promediaron ambas variables por hora del día (24 grupos) y se calculó la correlación de Pearson en dos niveles: entre los 24 promedios horarios y entre las dos lecturas de un mismo ciclo de captura (n = 142.856 pares).",
        "resultado": "La temperatura promedio va de 12,14 °C (2 h) a 22,56 °C (15 h). La humedad relativa va de 84,10 % (2 h) a 68,42 % (18 h). La correlación es r = −0,99 entre promedios horarios y r = −0,84 entre lecturas del mismo ciclo.",
        "hallazgo": "Existe una asociación inversa fuerte: cuando sube la temperatura baja la humedad relativa. Las horas de 13 a 18 h combinan la mayor temperatura y la menor humedad.",
        "interpretacion": "La franja de la tarde es la de mayor demanda evaporativa del escenario, la más relevante para vigilar el invernadero. La correlación entre promedios (−0,99) es más alta que entre lecturas (−0,84) porque al promediar se elimina el ruido.",
        "utilidad": "Orienta el monitoreo y las acciones de ventilación o riego hacia la tarde.",
        "limitacion": "Es una asociación, no una causa. Ambas variables provienen del mismo sensor y del mismo generador de datos, que define sus ciclos diarios.",
        "grafico": "c3",
    },
    {
        "id": "C4",
        "titulo": "Con lluvia, la iluminación diurna cae alrededor de un 82 %",
        "analisis": "B3 · Análisis bivariado",
        "pagina": "Análisis bivariados",
        "pregunta": "¿Cómo cambia la iluminación diurna cuando se detecta lluvia? Permite saber si las alertas de iluminación responden a la lluvia o a otro factor.",
        "variables": "VAR-004 Iluminación (lux) del BH1750; condicion_lluvia (columna calculada a partir de VAR-006 en el mismo ciclo); es_diurna de DIM_HORA.",
        "procedimiento": "Cada lectura se marcó «Con lluvia» si su ciclo de captura registró agua en VAR-006 (16.200 ciclos). Se comparó el promedio y la mediana de iluminación entre 6 y 17 h con y sin lluvia. Para descartar el efecto de la hora, se repitió la comparación solo entre 12 y 17 h.",
        "resultado": "Promedio 6–17 h: 802,69 lux sin lluvia (n = 56.456) frente a 148,62 lux con lluvia (n = 10.800), −81,5 %. Control 12–17 h: 828,22 frente a 148,62 lux, −82,1 %. Lecturas menores de 150 lux: 3,3 % sin lluvia y 47,0 % con lluvia. El 79,8 % de las alertas de iluminación (644 de 807) ocurrió con lluvia.",
        "hallazgo": "La lluvia se asocia con una caída cercana al 82 % de la luz diurna, y esa diferencia se mantiene al controlar la hora.",
        "interpretacion": "La mayoría de las alertas de iluminación coincide con episodios de lluvia y no con fallas del sensor. Una alerta de iluminación con lluvia es esperable; sin lluvia merece revisión.",
        "utilidad": "Permite cruzar la alerta de iluminación con el sensor de lluvia para filtrar alertas esperadas.",
        "limitacion": "El resultado reproduce el factor de 0,18 programado en el generador. Hay solo tres bloques de lluvia y el BH1750 está en el acceso del invernadero, no sobre las parcelas.",
        "grafico": "c4",
    },
    {
        "id": "C5",
        "titulo": "Las alertas se concentran en la Parcela 2 y en la noche",
        "analisis": "M1 · Análisis multivariado",
        "pagina": "Análisis multivariado",
        "pregunta": "¿En qué ubicación, franja del día y tipo de dispositivo se concentran las alertas? Permite dirigir la atención a una zona y un horario concretos.",
        "variables": "nombre_ubicacion (DIM_UBICACION), tipo_dispositivo (DIM_DISPOSITIVO), franja_dia (DIM_HORA), Alertas y Alertas por 1.000 mediciones.",
        "procedimiento": "En una matriz de Power BI se calcularon las alertas y la tasa por 1.000 mediciones para cada combinación de ubicación, tipo de dispositivo y franja, directamente sobre la tabla de hechos. El resultado se reprodujo en SQL Server con GROUP BY ROLLUP y coincidió exactamente.",
        "resultado": "Parcela 2 concentra 18.466 alertas (73,4 %) y 129,26 por 1.000 mediciones. La noche reúne 13.156 alertas (52,3 %). La celda Parcela 2–noche tiene 7.976 alertas (31,7 % del total) y 246,17 por 1.000 mediciones. Todas las alertas provienen de dispositivos tipo SENSOR.",
        "hallazgo": "La combinación Parcela 2 + noche es la de mayor concentración. Al aplicar histéresis, ambas parcelas tienen casi los mismos episodios (4.636 y 4.678): la Parcela 2 no tiene más episodios secos, sino episodios más largos que generan más cruces del umbral.",
        "interpretacion": "La Parcela 2 permanece más tiempo por encima de 3.300 ADC (sustrato más seco), sobre todo de noche, cuando el sustrato alcanza su máximo diario hacia las 20 h. Para comparar parcelas, el % de lecturas ≥ 3.300 es mejor indicador que el número de alertas.",
        "utilidad": "Sustenta la decisión D2: un riego diferenciado para la Parcela 2 antes del pico nocturno.",
        "limitacion": "La variable tipo_dispositivo no discrimina (todas las alertas son de SENSOR). El pico nocturno sigue la fase programada en el generador y la base más seca de la Parcela 2 (3.260 frente a 3.150 ADC) también es un parámetro de la simulación.",
        "grafico": "c5",
    },
]

# ---------------------------------------------------------------------------
# Decisiones sustentadas
# ---------------------------------------------------------------------------
DECISIONES = [
    {
        "id": "D1",
        "titulo": "Rediseñar la alerta de humedad del sustrato con histéresis",
        "accion": "Activar la alerta cuando la lectura sea ≥ 3.300 ADC y rearmarla solo cuando baje de 3.200 ADC. Como opción, confirmar la condición con 3 lecturas consecutivas.",
        "hallazgo": "C2 y la validación de la regla: 24.339 alertas de sustrato (95,14 % de los eventos). Con histéresis 3.300/3.200 pasarían a 9.314 (−61,7 %) y la tasa total bajaría de 25,15 a 10,12 alertas por 1.000 mediciones.",
        "dirigida": "Proceso PRO-002 Monitoreo del sustrato; dispositivos DIS-001 y DIS-002 (Parcelas 1 y 2); regla del generador y firmware del ESP32.",
        "mejora": "Pasar de unas 7.400 a unas 2.800 alertas de sustrato por día, conservando un aviso por cada episodio seco.",
        "indicador": "Alertas por 1.000 mediciones (línea base 25,15; meta ≤ 10,5) y alertas de sustrato por día (meta ≤ 3.000).",
        "limitaciones": "Es un recálculo retrospectivo sobre datos simulados. El umbral de 3.300 ADC no está calibrado contra contenido de agua, y la banda de histéresis debe ajustarse al ruido real de los sensores.",
        "grafico": "d1",
    },
    {
        "id": "D2",
        "titulo": "Riego diferenciado para la Parcela 2 entre las 16 y las 18 h",
        "accion": "Programar un riego adicional para la Parcela 2 entre las 16 y las 18 h, antes del máximo nocturno del sustrato, en un piloto de 2 semanas con la Parcela 1 como referencia.",
        "hallazgo": "B2 y C5: la Parcela 2 tiene 25,82 % de lecturas ≥ 3.300 ADC frente a 4,67 % de la Parcela 1; de noche, 64,6 % frente a 18,3 %. Su promedio es 3.217,41 frente a 3.098,81 ADC, y la celda Parcela 2–noche concentra 7.976 alertas.",
        "dirigida": "Ubicación UBI-002 Parcela 2; dispositivo DIS-002; proceso PRO-002; franja tarde-noche.",
        "mejora": "Reducir el tiempo que la Parcela 2 pasa por encima de 3.300 ADC durante la noche.",
        "indicador": "% de lecturas de sustrato ≥ 3.300 ADC en la Parcela 2 de noche (línea base 64,6 %; meta ≤ 20 %), con la medida DAX «% Lecturas sustrato >= 3300».",
        "limitaciones": "El generador asigna a la Parcela 2 una base más seca (3.260 frente a 3.150 ADC). No hay registros de riego ni calibración de los sensores, y la relación observada es una asociación, no una causa demostrada.",
        "grafico": "d2",
    },
]

MEDIDA_D2 = """% Lecturas sustrato >= 3300 =
DIVIDE (
    CALCULATE ( [Mediciones],
        DIM_CONCEPTO[codigo_concepto] = "VAR-003",
        FACT_REGISTRO_AGROSMART[valor_numerico] >= 3300 ),
    CALCULATE ( [Mediciones], DIM_CONCEPTO[codigo_concepto] = "VAR-003" ) )"""

SQL_M1 = """USE [AgroSmart DW];
SELECT u.nombre_ubicacion, h.franja_dia, SUM(f.cantidad_eventos) AS alertas
FROM dbo.FACT_REGISTRO_AGROSMART f
JOIN dbo.DIM_UBICACION u ON u.ubicacion_key = f.ubicacion_key
JOIN dbo.DIM_HORA      h ON h.hora_key      = f.hora_key
JOIN dbo.DIM_CONCEPTO  c ON c.concepto_key  = f.concepto_key
WHERE c.codigo_concepto IN ('ALERTA_HUMEDAD_SUSTRATO','ALERTA_TEMPERATURA','ALERTA_ILUMINACION')
  AND f.fecha_hora_registro >= '20261101' AND f.fecha_hora_registro < '20261105'
GROUP BY ROLLUP (u.nombre_ubicacion, h.franja_dia)
ORDER BY u.nombre_ubicacion, h.franja_dia;"""

MEDIDAS_DAX = """Mediciones = SUM ( FACT_REGISTRO_AGROSMART[cantidad_mediciones] )
Eventos    = SUM ( FACT_REGISTRO_AGROSMART[cantidad_eventos] )
Alertas    = CALCULATE ( [Eventos],
    DIM_CONCEPTO[codigo_concepto] IN
        { "ALERTA_HUMEDAD_SUSTRATO", "ALERTA_TEMPERATURA", "ALERTA_ILUMINACION" } )
% Alertas sobre eventos        = DIVIDE ( [Alertas], [Eventos] )
Alertas por 1.000 mediciones   = DIVIDE ( [Alertas], [Mediciones] ) * 1000
Dispositivos activos = CALCULATE ( DISTINCTCOUNT ( FACT_REGISTRO_AGROSMART[dispositivo_key] ),
    FACT_REGISTRO_AGROSMART[tipo_registro] = "MEDICION" )
Temperatura promedio (°C) = CALCULATE ( AVERAGE ( FACT_REGISTRO_AGROSMART[valor_numerico] ),
    DIM_CONCEPTO[codigo_concepto] = "VAR-001" )
Lecturas con lluvia = CALCULATE ( [Mediciones],
    DIM_CONCEPTO[codigo_concepto] = "VAR-006",
    FACT_REGISTRO_AGROSMART[valor_numerico] = 0 )
% Lecturas con lluvia = DIVIDE ( [Lecturas con lluvia],
    CALCULATE ( [Mediciones], DIM_CONCEPTO[codigo_concepto] = "VAR-006" ) )"""

FILTRO_M = """#"Filas filtradas" = Table.SelectRows(dbo_FACT_REGISTRO_AGROSMART,
    each [fecha_hora_registro] >= #datetime(2026,11,1,0,0,0)
     and [fecha_hora_registro] <  #datetime(2026,11,5,0,0,0))"""

COLUMNAS_DAX = """-- Ordena las franjas del día (DIM_HORA)
orden_franja = SWITCH ( TRUE (),
    DIM_HORA[hora] <= 5, 1, DIM_HORA[hora] <= 11, 2, DIM_HORA[hora] <= 17, 3, 4 )

-- Ciclos de captura que detectaron agua (tabla calculada, 16.200 filas)
CiclosConLluvia = CALCULATETABLE (
    VALUES ( FACT_REGISTRO_AGROSMART[id_ciclo_captura] ),
    DIM_CONCEPTO[codigo_concepto] = "VAR-006",
    FACT_REGISTRO_AGROSMART[valor_numerico] = 0 )

-- Marca cada medición según la condición de lluvia de su ciclo
condicion_lluvia = IF ( ISBLANK ( FACT_REGISTRO_AGROSMART[id_ciclo_captura] ), BLANK (),
    IF ( FACT_REGISTRO_AGROSMART[id_ciclo_captura] IN CiclosConLluvia,
         "Con lluvia", "Sin lluvia" ) )"""

# ---------------------------------------------------------------------------
# Referencias (APA 7)
# ---------------------------------------------------------------------------
REFERENCIAS = [
    {"cita": "Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C. y Wirth, R. (2000). <i>CRISP-DM 1.0: Step-by-step data mining guide</i>. SPSS.", "url": None},
    {"cita": "Farooq, M. S., Riaz, S., Abid, A., Abid, K. y Naeem, M. A. (2019). A survey on the role of IoT in agriculture for the implementation of smart farming. <i>IEEE Access, 7</i>, 156237–156271.", "url": "https://doi.org/10.1109/ACCESS.2019.2949703"},
    {"cita": "Food and Agriculture Organization of the United Nations. (s. f.). <i>Coping with water scarcity: The role of agriculture – Phase 1</i>. AQUASTAT. Recuperado el 14 de noviembre de 2026, de", "url": "https://www.fao.org/aquastat/en/activities/prev-projects/cws-phase1"},
    {"cita": "Kamilaris, A., Kartakoullis, A. y Prenafeta-Boldú, F. X. (2017). A review on the practice of big data analysis in agriculture. <i>Computers and Electronics in Agriculture, 143</i>, 23–37.", "url": "https://doi.org/10.1016/j.compag.2017.09.037"},
    {"cita": "Kimball, R. y Ross, M. (2013). <i>The data warehouse toolkit: The definitive guide to dimensional modeling</i> (3.ª ed.). John Wiley & Sons.", "url": None},
    {"cita": "Microsoft. (s. f.-a). <i>Embed a report in a secure portal or website</i>. Microsoft Learn. Recuperado el 14 de noviembre de 2026, de", "url": "https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-embed-secure"},
    {"cita": "Microsoft. (s. f.-b). <i>Publish to web from Power BI</i>. Microsoft Learn. Recuperado el 14 de noviembre de 2026, de", "url": "https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-publish-to-web"},
    {"cita": "Microsoft. (s. f.-c). <i>Understand star schema and the importance for Power BI</i>. Microsoft Learn. Recuperado el 14 de noviembre de 2026, de", "url": "https://learn.microsoft.com/en-us/power-bi/guidance/star-schema"},
    {"cita": "Microsoft. (s. f.-d). <i>Use grouping and binning in Power BI Desktop</i>. Microsoft Learn. Recuperado el 14 de noviembre de 2026, de", "url": "https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-grouping-and-binning"},
    {"cita": "Microsoft. (2026a, 21 de enero). <i>Error handling in data</i>. Microsoft Learn.", "url": "https://learn.microsoft.com/en-us/sql/integration-services/data-flow/error-handling-in-data"},
    {"cita": "Microsoft. (2026b, 22 de enero). <i>Conditional Split transformation</i>. Microsoft Learn.", "url": "https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/conditional-split-transformation"},
    {"cita": "Microsoft. (2026c, 22 de enero). <i>Lookup transformation</i>. Microsoft Learn.", "url": "https://learn.microsoft.com/en-us/sql/integration-services/data-flow/transformations/lookup-transformation"},
    {"cita": "Placidi, P., Gasperini, L., Grassi, A., Cecconi, M. y Scorzoni, A. (2020). Characterization of low-cost capacitive soil moisture sensors for IoT networks. <i>Sensors, 20</i>(12), 3585.", "url": "https://doi.org/10.3390/s20123585"},
    {"cita": "Universidad de Cundinamarca. (2023). <i>Lineamientos para la planificación, ejecución y evaluación de los proyectos de gestión del conocimiento (PGC) en la Facultad de Ingeniería</i> [Comunicado N.° 03]. Facultad de Ingeniería.", "url": None},
    {"cita": "Wolfert, S., Ge, L., Verdouw, C. y Bogaardt, M.-J. (2017). Big data in smart farming – A review. <i>Agricultural Systems, 153</i>, 69–80.", "url": "https://doi.org/10.1016/j.agsy.2017.01.023"},
]

# ---------------------------------------------------------------------------
# Navegación
# ---------------------------------------------------------------------------
# Orden de lectura del PGC: se usa para los botones «Anterior / Siguiente».
SECUENCIA = [
    ("main.home", "Inicio"),
    ("project.overview", "Identificación, problema y objetivos"),
    ("project.framework", "Marco referencial"),
    ("project.methodology", "Metodología y cronograma"),
    ("project.solution", "Desarrollo de la solución"),
    ("project.data", "Gestión de los datos"),
    ("monitoring.dashboard", "Monitoreo"),
    ("analytics.preparation", "Preparación del análisis"),
    ("analytics.dashboard", "Dashboard de Power BI"),
    ("analytics.knowledge", "Conocimientos evidentes"),
    ("analytics.decisions", "Validación y decisiones"),
    ("results.products", "Productos y resultados"),
    ("results.conclusions", "Conclusiones y referencias"),
    ("main.about", "Acerca de"),
]

MENU = [
    {"label": "Inicio", "endpoint": "main.home"},
    {"label": "Proyecto", "blueprint": "project", "children": [
        ("project.overview", "Identificación, problema y objetivos"),
        ("project.framework", "Marco referencial"),
        ("project.methodology", "Metodología y cronograma"),
        ("project.solution", "Desarrollo de la solución"),
        ("project.data", "Gestión de los datos"),
    ]},
    {"label": "Monitoreo", "endpoint": "monitoring.dashboard", "blueprint": "monitoring"},
    {"label": "Analítica", "blueprint": "analytics", "children": [
        ("analytics.preparation", "Preparación del análisis"),
        ("analytics.dashboard", "Dashboard de Power BI"),
        ("analytics.knowledge", "Conocimientos evidentes"),
        ("analytics.decisions", "Validación y decisiones"),
    ]},
    {"label": "Resultados", "blueprint": "results", "children": [
        ("results.products", "Productos y resultados"),
        ("results.conclusions", "Conclusiones y referencias"),
    ]},
    {"label": "Acerca de", "endpoint": "main.about"},
]
