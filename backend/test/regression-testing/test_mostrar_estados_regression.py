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

@patch("src.routes.vista_perfil.actualizar_estado_dispositivo")
def test_regression_mostrar_estados_dispositivos(mock_actualizar, client, snapshot):
    """
    Prueba de regresión para Mostrar/Actualizar estados (PUT /perfil/dispositivo/<id>/estado).
    """
    mock_actualizar.return_value = True

    payload = {
        "estado_activo": True
    }

    with client.session_transaction() as sess:
        sess['usuario'] = {"id": 1}

    response = client.put("/perfil/dispositivo/10/estado", json=payload)
    
    assert response.status_code == 200
    mock_actualizar.assert_called_once_with(10, 1, True)
    assert response.json == snapshot
