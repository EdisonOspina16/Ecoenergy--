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
def test_regression_listar_dispositivos_conectados(mock_obtener_disp, mock_obtener_hogar, client, snapshot):
    """
    Prueba de regresión para Listar dispositivos (GET /perfil).
    """
    mock_obtener_hogar.return_value = None

    mock_disp1 = MagicMock()
    mock_disp1.to_dict.return_value = {"id_dispositivo": 10, "alias": "TV", "estado_activo": False}
    mock_disp2 = MagicMock()
    mock_disp2.to_dict.return_value = {"id_dispositivo": 11, "alias": "PC", "estado_activo": True}
    
    mock_obtener_disp.return_value = [mock_disp1, mock_disp2]

    with client.session_transaction() as sess:
        sess['usuario'] = {"id": 1}

    response = client.get("/perfil")
    
    assert response.status_code == 200
    assert response.json == snapshot
