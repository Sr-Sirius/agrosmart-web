# AgroSmart Web

Aplicación web inicial de AgroSmart, módulo agropecuario de la ciudad inteligente NEOGRID.

## Estado actual

El sitio documenta el Proyecto de Gestión del Conocimiento (PGC) de AgroSmart e integra el dashboard de Power BI:

- **Proyecto:** identificación, problema, justificación y objetivos; marco referencial; metodología CRISP-DM y cronograma; desarrollo de la solución; gestión de los datos (MER, simulación, Data Warehouse y ETL en SSIS).
- **Monitoreo:** variables del módulo con el resumen del periodo simulado. La recepción en vivo desde el ESP32 queda para una fase posterior.
- **Analítica:** preparación del análisis, dashboard de Power BI insertado, cinco conocimientos evidentes, validación y dos decisiones sustentadas.
- **Resultados:** productos y evidencias, conclusiones y referencias en APA 7.

Todos los textos y cifras están en `app/content.py`. Las cifras provienen de AgroSmart DW (periodo simulado del 01/11/2026 al 04/11/2026) y no deben cambiarse sin recalcularlas.

## Requisitos

- Python 3.12.11 (versión fijada en `.python-version` para mantener un entorno reproducible entre desarrollo y Render).
- pip.

## Ejecución local en Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python -m flask --app wsgi run --debug
```

Abrir `http://127.0.0.1:5000`.

Si PowerShell bloquea la activación del entorno virtual, se puede ejecutar directamente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app wsgi run --debug
```

## Despliegue en Render

Crear un servicio de tipo **Web Service** y conectar este repositorio de GitHub.

- Runtime: Python 3.
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn wsgi:app`
- Root Directory: dejar vacío si el proyecto está en la raíz del repositorio.

La aplicación exporta el objeto Flask `app` desde `wsgi.py`, por eso Gunicorn utiliza `wsgi:app`.

## Variables de entorno

Configurar en Render cuando corresponda:

- `SECRET_KEY`: clave aleatoria para la aplicación.
- `POWERBI_EMBED_URL`: URL de inserción del informe de Power BI (solo el valor de `src` del iframe). Dejar vacía mientras el informe no esté listo.
  - Con **Publicar en la web**: `https://app.powerbi.com/view?r=...` (cualquier persona puede verlo sin iniciar sesión).
  - Con **Insertar informe > Sitio web o portal**: `https://app.powerbi.com/reportEmbed?reportId=...&autoAuth=true&ctid=...` (quien lo abra debe iniciar sesión y tener permiso; compartir el informe con el docente).
  - Después de cambiar la variable en Render, el servicio se vuelve a desplegar y el iframe aparece en `/analitica/`.

No guardar secretos, contraseñas, cadenas de conexión ni archivos `.env` en GitHub.

## Estructura

```text
app/
  __init__.py          # fábrica de la app, menú, filtro de números y navegación anterior/siguiente
  config.py
  content.py           # textos, cifras, conocimientos, decisiones y referencias del sitio
  routes/
    main.py            # /  y  /acerca
    project.py         # /proyecto/, /proyecto/marco-referencial, /metodologia, /solucion, /datos
    monitoring.py      # /monitoreo/
    analytics.py       # /analitica/, /analitica/preparacion, /conocimientos, /validacion-decisiones
    results.py         # /resultados/, /resultados/conclusiones
  templates/
    base.html
    index.html, monitoreo.html, acerca.html
    proyecto/          # páginas del PGC
    analitica/         # dashboard, preparación, conocimientos y decisiones
    resultados/        # productos y conclusiones
    macros/            # componentes de interfaz y gráficos SVG
    errors/
  static/
    css/styles.css
    js/main.js
    img/               # fotos del prototipo y evidencias de los informes
tests/
  test_routes.py
wsgi.py
requirements.txt
.python-version
.env.example
.gitignore
```

## Pruebas

```powershell
pip install pytest
python -m pytest -q
```

Las pruebas comprueban que todas las páginas respondan, que estén los cinco conocimientos y las dos decisiones, y que el iframe use `POWERBI_EMBED_URL`.

## Trabajo colaborativo sugerido

- `main`: versión estable.
- `develop`: integración del equipo y rama conectada inicialmente a Render.
- `feature/*`: cambios concretos por integrante.

Integrar los cambios mediante Pull Requests hacia `develop`. Cuando una versión esté validada, fusionarla en `main`.

## Próximas integraciones

1. API para recibir lecturas del ESP32 por Wi-Fi y registrarlas en AgroSmartDB con origen REAL.
2. Acceso seguro a los datos operacionales de AgroSmart.
3. Carga incremental hacia AgroSmart DW y actualización del dashboard.
4. Última lectura de cada sensor en la página de monitoreo.
