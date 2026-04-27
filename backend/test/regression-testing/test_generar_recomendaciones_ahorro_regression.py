import pytest
from flask import Flask
from unittest.mock import patch
from src.routes.vista_consumo import vista_consumo

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(vista_consumo)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@patch("src.routes.vista_consumo.procesar_recomendacion")
def test_regression_generar_recomendaciones_ahorro(mock_procesar, client, snapshot):
    """
    Prueba de regresión para Generar Recomendaciones de Ahorro por dispositivo (POST /recomendacion).
    """
    mock_procesar.return_value = {
        "recomendacion": "Deberías reducir el uso del televisor.",
        "esAlerta": True,
        "dispositivo": "Televisor"
    }

    payload = {
        "consumo_watts": 800,
        "dispositivo": "Televisor"
    }

    response = client.post("/recomendacion", json=payload)
    
    assert response.status_code == 200
    assert response.json == snapshot
