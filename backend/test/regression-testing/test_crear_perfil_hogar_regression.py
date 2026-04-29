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

@patch("src.routes.vista_perfil.seleccionar_accion_perfil")
def test_regression_crear_perfil_hogar(mock_accion, client, snapshot):
    """
    Prueba de regresión para Crear perfil de hogar (POST /perfil).
    """
    mock_accion.return_value = ({"success": True, "message": "Perfil creado exitosamente"}, 200)

    payload = {
        "address": "Calle 123",
        "nombre_hogar": "Hogar Dulce Hogar"
    }

    with client.session_transaction() as sess:
        sess['usuario'] = {"id": 1}

    response = client.post("/perfil", json=payload)
    
    assert response.status_code == 200
    assert response.json == snapshot
