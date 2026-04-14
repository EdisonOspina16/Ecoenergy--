import pytest
from flask import Flask, json
from unittest.mock import patch
from src.routes.vista_consumo import vista_consumo

# Una app de Flask para realizar peticiones reales a la vista Blueprint
@pytest.fixture
def client():
    app = Flask(__name__)
    app.secret_key = "test_secret" # NOSONAR - Solo para pruebas, no usar en producción
    app.register_blueprint(vista_consumo)
    
    # Creamos un dummy de la condición de sesión para el decorator @login_requerido
    @app.before_request
    def mocker_sesion():
        from flask import session
        session["usuario"] = {"id": 1}
        
    with app.test_client() as client:
        yield client

class TestVistaConsumo:

    # ---------------------------------------------------------
    # Test GET: /ahorro-estimado
    # ---------------------------------------------------------
    @patch('src.routes.vista_consumo.procesar_ahorro_estimado')
    def test_ahorro_estimado_exito(self, mock_procesar, client):
        mock_procesar.return_value = {"ahorro": "100"}
        
        response = client.get("/ahorro-estimado")
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["success"] is True
        assert data["data"] == {"ahorro": "100"}

    @patch('src.routes.vista_consumo.procesar_ahorro_estimado')
    def test_ahorro_estimado_valor_invalido(self, mock_procesar, client):
        mock_procesar.side_effect = ValueError("Dispositivos no encontrados")
        
        response = client.get("/ahorro-estimado")
        data = response.get_json()
        
        assert response.status_code == 400
        assert data["success"] is False

    @patch('src.routes.vista_consumo.procesar_ahorro_estimado')
    def test_ahorro_estimado_error_interno(self, mock_procesar, client):
        mock_procesar.side_effect = Exception("Error fatal")
        
        response = client.get("/ahorro-estimado")
        data = response.get_json()
        
        assert response.status_code == 500
        assert data["success"] is False


    # ---------------------------------------------------------
    # Test POST: /recomendacion
    # ---------------------------------------------------------
    @patch('src.routes.vista_consumo.procesar_recomendacion')
    def test_recomendacion_exito(self, mock_procesar, client):
        mock_procesar.return_value = {"recomendacion": "Ok"}
        
        response = client.post("/recomendacion", json={"consumo_watts": 100, "dispositivo": "TV"})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["recomendacion"] == "Ok"

    @patch('src.routes.vista_consumo.procesar_recomendacion')
    def test_recomendacion_error_interno(self, mock_procesar, client):
        mock_procesar.side_effect = Exception("DB caida")
        
        response = client.post("/recomendacion", json={})
        
        assert response.status_code == 500


    # ---------------------------------------------------------
    # Test GET: /recomendacion-diaria
    # ---------------------------------------------------------
    @patch('src.routes.vista_consumo.obtener_recomendacion_diaria_hogar_por_usuario')
    def test_obtener_recomendacion_diaria_exito(self, mock_obtener, client):
        mock_obtener.return_value = {"encontrado": True, "datos": "x"}
        
        response = client.get("/recomendacion-diaria")
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["encontrado"] is True

    @patch('src.routes.vista_consumo.obtener_recomendacion_diaria_hogar_por_usuario')
    def test_obtener_recomendacion_diaria_error(self, mock_obtener, client):
        mock_obtener.side_effect = Exception("Error en repo")
        
        response = client.get("/recomendacion-diaria")
        assert response.status_code == 500


    # ---------------------------------------------------------
    # Test POST: /recomendacion-diaria/generar
    # ---------------------------------------------------------
    @patch('src.routes.vista_consumo.generar_y_guardar_recomendacion_diaria')
    def test_generar_recomendacion_diaria_exito(self, mock_generar, client):
        mock_generar.return_value = {"generada": True}
        
        response = client.post("/recomendacion-diaria/generar")
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["success"] is True

    @patch('src.routes.vista_consumo.generar_y_guardar_recomendacion_diaria')
    def test_generar_recomendacion_diaria_value_error(self, mock_generar, client):
        mock_generar.side_effect = ValueError("Sin hogar")
        
        response = client.post("/recomendacion-diaria/generar")
        assert response.status_code == 400

    @patch('src.routes.vista_consumo.generar_y_guardar_recomendacion_diaria')
    def test_generar_recomendacion_diaria_error_interno(self, mock_generar, client):
        mock_generar.side_effect = Exception("Error 500")
        
        response = client.post("/recomendacion-diaria/generar")
        assert response.status_code == 500
