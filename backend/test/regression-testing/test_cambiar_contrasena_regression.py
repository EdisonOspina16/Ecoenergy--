import pytest
from flask import Flask
from unittest.mock import patch
from src.routes.vista_usuarios import blueprint_Usuarios

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test_key"
    app.register_blueprint(blueprint_Usuarios)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@patch("src.routes.vista_usuarios.cambiar_contrasena")
def test_regression_cambiar_contrasena(mock_cambiar, client, snapshot):
    """
    Prueba de regresión para Cambiar contraseña.
    """
    mock_cambiar.return_value = True

    payload = {
        "correo": "recuperar@test.com",
        "nueva_contrasena": "NuevaSecreta123!"
    }

    response = client.post("/recuperar", json=payload)
    
    assert response.status_code == 200
    mock_cambiar.assert_called_once()
    assert response.json == snapshot
