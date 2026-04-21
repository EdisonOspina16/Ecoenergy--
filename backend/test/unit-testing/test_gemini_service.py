import pytest
import json
from unittest.mock import patch, MagicMock
from google.genai.errors import ClientError
from hamcrest import assert_that, is_, contains_string, equal_to

from src.infrastructure.ia.gemini_service import llamar_recomendacion, llamar_ahorro_estimado

class TestLlamarRecomendacion:
    
    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_recomendacion_exitosa(self, mock_generate_content):
        # Arrange
        consumo = 120.5
        dispositivo = "televisor"
        
        mock_response = MagicMock()
        mock_response.text = "El consumo está en los niveles normales."
        mock_generate_content.return_value = mock_response
        
        # Act
        resultado = llamar_recomendacion(consumo, dispositivo)
        
        # Assert
        mock_generate_content.assert_called_once()
        assert_that(resultado, contains_string("niveles normales"))

    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_recomendacion_error_api(self, mock_generate_content):
        # Arrange
        mock_generate_content.side_effect = ClientError("API Key inválida", 403)
        
        # Act
        resultado = llamar_recomendacion(500, "nevera")
        
        # Assert
        mock_generate_content.assert_called_once()
        assert_that(resultado, contains_string("No fue posible generar la recomendación"))

    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_recomendacion_error_inesperado(self, mock_generate_content):
        # Arrange
        mock_generate_content.side_effect = Exception("Fallo interno grave")
        
        # Act
        resultado = llamar_recomendacion(500, "nevera")
        
        # Assert
        mock_generate_content.assert_called_once()
        assert_that(resultado, contains_string("Ocurrió un error interno al generar la recomendación"))

class TestLlamarAhorroEstimado:
    
    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_ahorro_estimado_exitoso(self, mock_generate_content):
        # Arrange
        dispositivos = [{"nombre": "Nevera", "consumo_watts": 400}]
        
        mock_response = MagicMock()
        mock_response.text = '{"ahorro_financiero": "5.000 COP", "impacto_ambiental": "20 kg", "indicador_didactico": "1 árbol"}'
        mock_generate_content.return_value = mock_response
        
        # Act
        resultado = llamar_ahorro_estimado(dispositivos)
        
        # Assert
        mock_generate_content.assert_called_once()
        assert_that(resultado["impacto_ambiental"], is_(equal_to("20 kg")))
        assert_that(resultado["ahorro_financiero"], is_(equal_to("5.000 COP")))
        assert_that(resultado["indicador_didactico"], is_(equal_to("1 árbol")))

    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_ahorro_estimado_formato_incorrecto(self, mock_generate_content):
        # Arrange
        dispositivos = [{"nombre": "Consola", "consumo_watts": 100}]
        
        mock_response = MagicMock()
        mock_response.text = "Esto no es un JSON"
        mock_generate_content.return_value = mock_response
        
        # Act
        resultado = llamar_ahorro_estimado(dispositivos)
        
        # Assert
        mock_generate_content.assert_called_once()
        assert_that(resultado["ahorro_financiero"], is_(equal_to("No disponible")))
        assert_that(resultado["impacto_ambiental"], is_(equal_to("No disponible")))

    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_ahorro_estimado_client_error(self, mock_generate_content):
        # Arrange
        dispositivos = [{"nombre": "PC", "consumo_watts": 200}]
        mock_generate_content.side_effect = ClientError("Timeout", 504)
        
        # Act
        resultado = llamar_ahorro_estimado(dispositivos)
        
        # Assert
        mock_generate_content.assert_called_once()
        assert_that(resultado["ahorro_financiero"], is_(equal_to("Error de conexión")))

    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_ahorro_estimado_exception(self, mock_generate_content):
        # Arrange
        dispositivos = [{"nombre": "PC", "consumo_watts": 200}]
        mock_generate_content.side_effect = Exception("System Crash")
        
        # Act
        resultado = llamar_ahorro_estimado(dispositivos)
        
        # Assert
        mock_generate_content.assert_called_once()
        assert_that(resultado["ahorro_financiero"], is_(equal_to("Error interno")))
