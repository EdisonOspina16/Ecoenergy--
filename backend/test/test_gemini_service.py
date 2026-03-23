import pytest
import json
from unittest.mock import patch, MagicMock
from google.genai.errors import ClientError

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
        assert "niveles normales" in resultado

    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_recomendacion_error_api(self, mock_generate_content):
        # Arrange
        mock_generate_content.side_effect = ClientError("API Key inválida", 403)
        
        # Act
        resultado = llamar_recomendacion(500, "nevera")
        
        # Assert
        mock_generate_content.assert_called_once()
        assert "No fue posible generar la recomendación" in resultado

    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_recomendacion_error_inesperado(self, mock_generate_content):
        # Arrange
        mock_generate_content.side_effect = Exception("Fallo interno grave")
        
        # Act
        resultado = llamar_recomendacion(500, "nevera")
        
        # Assert
        mock_generate_content.assert_called_once()
        assert "Ocurrió un error interno al generar la recomendación" in resultado

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
        assert resultado["impacto_ambiental"] == "20 kg"
        assert resultado["ahorro_financiero"] == "5.000 COP"
        assert resultado["indicador_didactico"] == "1 árbol"

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
        assert resultado["ahorro_financiero"] == "No disponible"
        assert resultado["impacto_ambiental"] == "No disponible"

    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_ahorro_estimado_client_error(self, mock_generate_content):
        # Arrange
        dispositivos = [{"nombre": "PC", "consumo_watts": 200}]
        mock_generate_content.side_effect = ClientError("Timeout", 504)
        
        # Act
        resultado = llamar_ahorro_estimado(dispositivos)
        
        # Assert
        mock_generate_content.assert_called_once()
        assert resultado["ahorro_financiero"] == "Error de conexión"

    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_ahorro_estimado_exception(self, mock_generate_content):
        # Arrange
        dispositivos = [{"nombre": "PC", "consumo_watts": 200}]
        mock_generate_content.side_effect = Exception("System Crash")
        
        # Act
        resultado = llamar_ahorro_estimado(dispositivos)
        
        # Assert
        mock_generate_content.assert_called_once()
        assert resultado["ahorro_financiero"] == "Error interno"
