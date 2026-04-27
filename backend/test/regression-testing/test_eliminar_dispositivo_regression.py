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

@patch("src.routes.vista_perfil.eliminar_dispositivo")
def test_regression_eliminar_dispositivo(mock_eliminar, client, snapshot):
    """
    Prueba de regresión para Eliminar dispositivo (DELETE /perfil/dispositivo/<id>).
    """
    mock_eliminar.return_value = True

    with client.session_transaction() as sess:
        sess['usuario'] = {"id": 1}

    response = client.delete("/perfil/dispositivo/5")
    
    assert response.status_code == 200
    mock_eliminar.assert_called_once_with(5, 1)
    assert response.json == snapshot
