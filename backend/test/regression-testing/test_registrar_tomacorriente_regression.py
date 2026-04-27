import pytest
from flask import Flask
from unittest.mock import patch
from src.routes.vista_perfil import blueprint_perfil

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test_key"
    app.register_blueprint(blueprint_perfil)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@patch("src.routes.vista_perfil.registrar_tomacorriente")
def test_regression_registrar_tomacorriente(mock_registrar, client, snapshot):
    """
    Prueba de regresión para Registrar tomacorriente (POST /perfil).
    """
    mock_registrar.return_value = ({"success": True, "message": "Dispositivo registrado exitosamente"}, 201)

    payload = {
        "deviceId": "dev_001",
        "nickname": "Toma Sala"
    }

    with client.session_transaction() as sess:
        sess['usuario'] = {"id": 1}

    response = client.post("/perfil", json=payload)
    
    assert response.status_code == 201
    assert response.json == snapshot
