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
def test_regression_generar_impacto_ambiental(mock_procesar, client, snapshot):
    """
    Prueba de regresión para Generar impacto ambiental.
    Extrae la parte de impacto ambiental de /ahorro-estimado.
    """
    mock_procesar.return_value = {
        "ahorro_financiero": "$50.00",
        "impacto_ambiental": "Menos huella de carbono",
        "indicador_didactico": "10 árboles salvados"
    }

    response = client.get("/ahorro-estimado")
    
    assert response.status_code == 200
    # Verificamos que la estructura general y en específico impacto_ambiental no cambie
    assert response.json["data"]["impacto_ambiental"] == snapshot
