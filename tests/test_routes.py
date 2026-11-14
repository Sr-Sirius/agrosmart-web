"""Pruebas básicas: todas las páginas del sitio responden y muestran su contenido clave.

Ejecutar con:  python -m pytest -q
"""

import pytest

from app import create_app

PAGINAS = {
    "/": "Datos inteligentes",
    "/proyecto/": "Planteamiento del problema",
    "/proyecto/marco-referencial": "Antecedentes",
    "/proyecto/metodologia": "Cronograma",
    "/proyecto/solucion": "Arquitectura",
    "/proyecto/datos": "Proceso ETL en SSIS",
    "/monitoreo/": "Temperatura",
    "/analitica/": "Dashboard de Power BI",
    "/analitica/preparacion": "Preguntas orientadoras",
    "/analitica/conocimientos": "Conocimientos evidentes",
    "/analitica/validacion-decisiones": "Decisiones sustentadas",
    "/resultados/": "Productos esperados",
    "/resultados/conclusiones": "Referencias",
    "/acerca": "Acerca de AgroSmart",
}


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


@pytest.mark.parametrize("ruta,texto", PAGINAS.items())
def test_paginas_responden(client, ruta, texto):
    respuesta = client.get(ruta)
    assert respuesta.status_code == 200
    assert texto in respuesta.get_data(as_text=True)


def test_cinco_conocimientos_y_dos_decisiones(client):
    html = client.get("/analitica/conocimientos").get_data(as_text=True)
    for clave in ("C1", "C2", "C3", "C4", "C5"):
        assert f'id="{clave}"' in html
    html = client.get("/analitica/validacion-decisiones").get_data(as_text=True)
    assert 'id="D1"' in html and 'id="D2"' in html


def test_dashboard_usa_variable_de_entorno():
    app = create_app()
    app.config.update(TESTING=True, POWERBI_EMBED_URL="https://app.powerbi.com/view?r=prueba")
    html = app.test_client().get("/analitica/").get_data(as_text=True)
    assert '<iframe title="Dashboard de Power BI de AgroSmart" src="https://app.powerbi.com/view?r=prueba"' in html


def test_pagina_inexistente(client):
    assert client.get("/no-existe").status_code == 404
