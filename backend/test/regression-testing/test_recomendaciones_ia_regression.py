import pytest
from flask import Flask
from unittest.mock import patch
from src.routes.vista_consumo import vista_consumo

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test_key"
    app.register_blueprint(vista_consumo)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@patch("src.routes.vista_consumo.obtener_recomendacion_diaria_hogar_por_usuario")
def test_regression_modulo_ia_recomendaciones(mock_obtener, client, snapshot):
    """
    Prueba de regresión para Módulo de IA / Recomendaciones (GET /recomendacion-diaria).
    """
    mock_obtener.return_value = {
        "recomendacion": "La IA sugiere apagar los equipos inactivos por la noche.",
        "fecha": "2026-04-27"
    }

    with client.session_transaction() as sess:
        sess['usuario'] = {"id": 1}

    response = client.get("/recomendacion-diaria")
    
    assert response.status_code == 200
    assert response.json == snapshot
