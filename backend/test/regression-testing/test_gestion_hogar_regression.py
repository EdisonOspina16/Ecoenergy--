import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
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

@patch("src.routes.vista_perfil.obtener_hogar_por_usuario")
@patch("src.routes.vista_perfil.obtener_dispositivos_por_usuario")
def test_regression_gestion_hogar(mock_obtener_disp, mock_obtener_hogar, client, snapshot):
    """
    Prueba de regresión para Gestión del hogar (GET /perfil).
    """
    mock_hogar = MagicMock()
    mock_hogar.to_dict.return_value = {"id_hogar": 1, "nombre_hogar": "Mi Hogar"}
    mock_obtener_hogar.return_value = mock_hogar

    mock_obtener_disp.return_value = []

    with client.session_transaction() as sess:
        sess['usuario'] = {"id": 1}

    response = client.get("/perfil")
    
    assert response.status_code == 200
    assert response.json == snapshot
