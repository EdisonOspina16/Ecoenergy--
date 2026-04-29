import pytest
from flask import Flask, json
from unittest.mock import patch
from hamcrest import assert_that, is_, equal_to
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

    # Test GET: /ahorro-estimado
    @patch('src.routes.vista_consumo.procesar_ahorro_estimado')
    def test_consultar_ahorro_estimado_exitosamente(self, mock_procesar, client):
        """CP-API-001: Consultar ahorro estimado retorna éxito con datos correctos."""
        # Arrange
        mock_procesar.return_value = {"ahorro": "100"}
        
        # Act
        response = client.get("/ahorro-estimado")
        data = response.get_json()
        
        # Assert
        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(data["success"], is_(True))
        assert_that(data["data"], is_(equal_to({"ahorro": "100"})))

    @patch('src.routes.vista_consumo.procesar_ahorro_estimado')
    def test_consultar_ahorro_estimado_con_error_de_validacion(self, mock_procesar, client):
        """CP-API-002: Error de validación al procesar ahorro estimado retorna 400."""
        # Arrange
        mock_procesar.side_effect = ValueError("Dispositivos no encontrados")
        
        # Act
        response = client.get("/ahorro-estimado")
        data = response.get_json()
        
        # Assert
        assert_that(response.status_code, is_(equal_to(400)))
        assert_that(data["success"], is_(False))

    @patch('src.routes.vista_consumo.procesar_ahorro_estimado')
    def test_consultar_ahorro_estimado_con_error_del_servidor(self, mock_procesar, client):
        """CP-API-003: Error inesperado al procesar ahorro estimado retorna 500."""
        # Arrange
        mock_procesar.side_effect = Exception("Error fatal")
        
        # Act
        response = client.get("/ahorro-estimado")
        data = response.get_json()
        
        # Assert
        assert_that(response.status_code, is_(equal_to(500)))
        assert_that(data["success"], is_(False))

    # Test POST: /recomendacion
    @patch('src.routes.vista_consumo.procesar_recomendacion')
    def test_obtener_recomendacion_de_ia_exitosamente(self, mock_procesar, client):
        """CP-API-004: Obtener recomendación puntual de IA retorna éxito."""
        # Arrange
        mock_procesar.return_value = {"recomendacion": "Ok"}
        
        # Act
        response = client.post("/recomendacion", json={"consumo_watts": 100, "dispositivo": "TV"})
        data = response.get_json()
        
        # Assert
        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(data["recomendacion"], is_(equal_to("Ok")))

    @patch('src.routes.vista_consumo.procesar_recomendacion')
    def test_obtener_recomendacion_de_ia_con_error_del_servidor(self, mock_procesar, client):
        """CP-API-005: Error de sistema al solicitar recomendación puntual retorna 500."""
        # Arrange
        mock_procesar.side_effect = Exception("DB caida")
        
        # Act
        response = client.post("/recomendacion", json={})
        
        # Assert
        assert_that(response.status_code, is_(equal_to(500)))

    # Test GET: /recomendacion-diaria
    @patch('src.routes.vista_consumo.obtener_recomendacion_diaria_hogar_por_usuario')
    def test_obtener_recomendacion_diaria_del_hogar_exitosamente(self, mock_obtener, client):
        """CP-API-006: Consultar recomendaciones diarias guardadas retorna éxito."""
        # Arrange
        mock_obtener.return_value = {"encontrado": True, "datos": "x"}
        
        # Act
        response = client.get("/recomendacion-diaria")
        data = response.get_json()
        
        # Assert
        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(data["encontrado"], is_(True))

    @patch('src.routes.vista_consumo.obtener_recomendacion_diaria_hogar_por_usuario')
    def test_obtener_recomendacion_diaria_con_error_del_servidor(self, mock_obtener, client):
        """CP-API-007: Error de sistema al consultar recomendación diaria retorna 500."""
        # Arrange
        mock_obtener.side_effect = Exception("Error en repo")
        
        # Act
        response = client.get("/recomendacion-diaria")
        
        # Assert
        assert_that(response.status_code, is_(equal_to(500)))

    # Test POST: /recomendacion-diaria/generar
    @patch('src.routes.vista_consumo.generar_y_guardar_recomendacion_diaria')
    def test_generar_y_guardar_recomendacion_diaria_exitosamente(self, mock_generar, client):
        """CP-API-008: Generar y guardar recomendación diaria retorna éxito."""
        # Arrange
        mock_generar.return_value = {"generada": True}
        
        # Act
        response = client.post("/recomendacion-diaria/generar")
        data = response.get_json()
        
        # Assert
        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(data["success"], is_(True))

    @patch('src.routes.vista_consumo.generar_y_guardar_recomendacion_diaria')
    def test_generar_recomendacion_diaria_sin_hogar_registrado(self, mock_generar, client):
        """CP-API-009: Intentar generar recomendación sin hogar registrado retorna 400."""
        # Arrange
        mock_generar.side_effect = ValueError("Sin hogar")
        
        # Act
        response = client.post("/recomendacion-diaria/generar")
        
        # Assert
        assert_that(response.status_code, is_(equal_to(400)))

    @patch('src.routes.vista_consumo.generar_y_guardar_recomendacion_diaria')
    def test_generar_recomendacion_diaria_con_error_del_servidor(self, mock_generar, client):
        """CP-API-010: Error de sistema al generar recomendación diaria retorna 500."""
        # Arrange
        mock_generar.side_effect = Exception("Error 500")
        
        # Act
        response = client.post("/recomendacion-diaria/generar")
        
        # Assert
        assert_that(response.status_code, is_(equal_to(500)))
