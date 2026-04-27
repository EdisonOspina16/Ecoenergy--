import pytest
from flask import Flask
from unittest.mock import patch
from src.routes.vista_consumo import vista_consumo

# Creamos una app de Flask de prueba
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(vista_consumo)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@patch("src.routes.vista_consumo.procesar_ahorro_estimado")
def test_regression_ahorro_estimado(mock_procesar, client, snapshot):
    """
    Prueba de regresión con Syrupy para el endpoint GET /ahorro-estimado.
    Garantiza que la estructura JSON de la respuesta no cambie inesperadamente.
    """
    # Arrange: Mockeamos el servicio subyacente para tener un output determinista
    mock_procesar.return_value = {
        "ahorro_financiero": "$50.00 al mes",
        "impacto_ambiental": "Menos huella de carbono",
        "indicador_didactico": "10 árboles salvados"
    }

    # Act: Hacemos la petición HTTP al endpoint
    response = client.get("/ahorro-estimado")

    # Assert: Comparamos el resultado JSON con el snapshot guardado
    assert response.status_code == 200
    assert response.json == snapshot


@patch("src.routes.vista_consumo.procesar_recomendacion")
def test_regression_recomendacion(mock_procesar, client, snapshot):
    """
    Prueba de regresión con Syrupy para el endpoint POST /recomendacion.
    Garantiza que el mapeo de entrada y el JSON de salida se mantengan constantes.
    """
    # Arrange
    mock_procesar.return_value = {
        "recomendacion": "Deberías apagar el aire acondicionado por las noches.",
        "esAlerta": False,
        "dispositivo": "Aire Acondicionado"
    }

    payload = {
        "consumo_watts": 1500,
        "dispositivo": "Aire Acondicionado"
    }

    # Act
    response = client.post("/recomendacion", json=payload)

    # Assert
    assert response.status_code == 200
    # Verificamos que el mock fue llamado correctamente (regresión de lógica)
    mock_procesar.assert_called_once_with(1500, "Aire Acondicionado")
    # Verificamos que la estructura JSON sea idéntica al snapshot
    assert response.json == snapshot
