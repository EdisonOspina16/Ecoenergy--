import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
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

@patch("src.routes.vista_usuarios.verificar_credenciales")
def test_regression_inicio_sesion(mock_verificar, client, snapshot):
    """
    Prueba de regresión para Inicio de sesión.
    """
    mock_user = MagicMock()
    mock_user.to_dict.return_value = {"id": 1, "correo": "login@test.com", "nombre": "Test"}
    mock_verificar.return_value = mock_user

    payload = {
        "correo": "login@test.com",
        "contrasena": "Secreta123!"
    }

    response = client.post("/login", json=payload)
    
    assert response.status_code == 200
    assert response.json == snapshot
