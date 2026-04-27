import pytest
from flask import Flask
from unittest.mock import patch
from src.routes.vista_consumo import vista_consumo

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(vista_consumo)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@patch("src.routes.vista_consumo.procesar_ahorro_estimado")
def test_regression_calcular_ahorro_economico(mock_procesar, client, snapshot):
    """
    Prueba de regresión para Calcular ahorro económico.
    """
    mock_procesar.return_value = {
        "ahorro_financiero": "$100.00 al mes",
        "impacto_ambiental": "Positivo",
        "indicador_didactico": "20 árboles"
    }

    response = client.get("/ahorro-estimado")
    
    assert response.status_code == 200
    assert response.json["data"]["ahorro_financiero"] == snapshot
