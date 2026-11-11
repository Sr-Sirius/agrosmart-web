# AgroSmart Web

Aplicación web inicial de AgroSmart, módulo agropecuario de la ciudad inteligente NEOGRID.

## Estado actual

Esta versión contiene la estructura base del sitio y páginas informativas. Todavía no conecta con el ESP32, la API de datos ni las bases SQL Server. La sección de analítica está preparada para recibir una URL de inserción de Power BI cuando el informe esté listo.

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
- `POWERBI_EMBED_URL`: URL de inserción autorizada del informe de Power BI. Dejar vacía mientras el informe no esté listo.

No guardar secretos, contraseñas, cadenas de conexión ni archivos `.env` en GitHub.

## Estructura

```text
app/
  __init__.py
  config.py
  routes/
    main.py
    project.py
    monitoring.py
    analytics.py
  templates/
    base.html
    index.html
    proyecto.html
    monitoreo.html
    analitica.html
    acerca.html
    errors/
  static/
    css/styles.css
    js/main.js
    img/
wsgi.py
requirements.txt
.python-version
.env.example
.gitignore
```

## Trabajo colaborativo sugerido

- `main`: versión estable.
- `develop`: integración del equipo y rama conectada inicialmente a Render.
- `feature/*`: cambios concretos por integrante.

Integrar los cambios mediante Pull Requests hacia `develop`. Cuando una versión esté validada, fusionarla en `main`.

## Próximas integraciones

1. API para recibir lecturas del ESP32.
2. Acceso seguro a los datos operacionales de AgroSmart.
3. Consultas a AgroSmart DW.
4. Integración del informe de Power BI.
5. Ampliación de las secciones de documentación y gestión del conocimiento.
