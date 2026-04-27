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

@patch("src.routes.vista_usuarios.registrar_usuario")
def test_regression_registro_usuario(mock_registrar, client, snapshot):
    """
    Prueba de regresión para Registro de usuario.
    Verifica que la salida y estructura JSON no cambien.
    """
    mock_registrar.return_value = True

    payload = {
        "nombre": "Test",
        "apellidos": "Usuario",
        "correo": "registro@test.com",
        "contrasena": "Secreta123!"
    }

    response = client.post("/registro", json=payload)
    
    assert response.status_code == 200
    mock_registrar.assert_called_once()
    assert response.json == snapshot
