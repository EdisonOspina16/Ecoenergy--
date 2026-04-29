import pytest
from flask import Flask
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

def test_regression_cerrar_sesion(client, snapshot):
    """
    Prueba de regresión para Cerrar sesión.
    """
    # Simulamos que hay una sesión iniciada
    with client.session_transaction() as sess:
        sess['usuario'] = {"id": 1, "correo": "test@test.com"}

    response = client.post("/logout")
    
    assert response.status_code == 200
    assert response.json == snapshot
