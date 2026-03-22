import pytest
import json
from unittest.mock import patch, MagicMock
from google.genai.errors import ClientError

# Importamos las funciones a probar del servicio real (gemini_service)
from src.infrastructure.ia.gemini_service import llamar_recomendacion, llamar_ahorro_estimado

"""
Explicación de Test Doubles usados:
1. **Dummy**: Datos inyectados (ej. 'dispositivos', 'consumos') para cumplir la firma de las funciones, sin importar mucho su valor en casos de error.
2. **Stub**: Usado mediante @patch a `client.models.generate_content`. Simula el comportamiento de la IA retornando valores "ideales" o "rotos" (como un JSON malformado o ClientError) según necesite el test, garantizando velocidad y aislamiento del internet.
3. **Mock**: El mismo @patch nos permite verificar las interacciones (ej: assert_called_once) para confirmar que se intentó contactar a Gemini con el modelo correcto.
"""

class TestLlamarRecomendacion:
    # --- CASO NORMAL ---
    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_recomendacion_exitosa(self, mock_generate_content):
        # Arrange (Preparar)
        consumo = 120.5  # Dummy
        dispositivo = "televisor"  # Dummy
        
        # Stub
        mock_response = MagicMock()
        mock_response.text = "El consumo está en los niveles normales."
        mock_generate_content.return_value = mock_response
        
        # Act (Ejecutar)
        resultado = llamar_recomendacion(consumo, dispositivo)
        
        # Assert (Verificar)
        assert "niveles normales" in resultado
        mock_generate_content.assert_called_once()  # Mock: verificamos interacción

    # --- CASO DE ERROR ---
    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_recomendacion_error_api(self, mock_generate_content):
        # Arrange
        # Stub: Forzamos la caída de la API de Gemini (simulamos 403, 429, etc)
        mock_generate_content.side_effect = ClientError("API Key inválida", 403)
        
        # Act
        resultado = llamar_recomendacion(500, "nevera")
        
        # Assert
        assert "No fue posible generar la recomendación" in resultado


class TestLlamarAhorroEstimado:
    
    # --- RF-014: Mostrar impacto ambiental ---
    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_rf014_mostrar_impacto_ambiental(self, mock_generate_content):
        # Arrange
        dispositivos = [{"nombre": "Nevera", "consumo_watts": 400}]
        
        # Stub
        mock_response = MagicMock()
        mock_response.text = '{"ahorro_financiero": "5.000 COP/mes", "impacto_ambiental": "20 kg CO2 menos", "indicador_didactico": "Como plantar 1 árbol"}'
        mock_generate_content.return_value = mock_response
        
        # Act
        resultado = llamar_ahorro_estimado(dispositivos)
        
        # Assert
        assert resultado["impacto_ambiental"] == "20 kg CO2 menos"

    # --- RF-015: Calcular ahorro económico ---
    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_rf015_calcular_ahorro_economico(self, mock_generate_content):
        # Arrange
        dispositivos = [{"nombre": "TV", "consumo_watts": 100}]
        
        # Stub (Simulando también las "```json" tags que a veces devuelve Gemini)
        mock_response = MagicMock()
        mock_response.text = '```json\n{"ahorro_financiero": "10.000 COP", "impacto_ambiental": "5 kg CO2", "indicador_didactico": "1 hora menos"}\n```'
        mock_generate_content.return_value = mock_response
        
        # Act
        resultado = llamar_ahorro_estimado(dispositivos)
        
        # Assert
        assert resultado["ahorro_financiero"] == "10.000 COP"

    # --- RF-016: Mostrar huella de carbono ---
    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_rf016_mostrar_huella_carbono_valor_por_defecto(self, mock_generate_content):
        # Arrange
        # Simulamos que Gemini retorna un JSON pero olvida enviar impacto_ambiental
        dispositivos = [{"nombre": "Licuadora", "consumo_watts": 300}]
        
        mock_response = MagicMock()
        mock_response.text = '{"ahorro_financiero": "5.000 COP"}'  
        mock_generate_content.return_value = mock_response
        
        # Act
        resultado = llamar_ahorro_estimado(dispositivos)
        
        # Assert: el servicio debe usar el fallback con dict.get() sin romperse
        assert resultado["impacto_ambiental"] == "N/A"
        assert resultado["indicador_didactico"] == "N/A"

    # --- CASO DE ERROR ---
    @patch('src.infrastructure.ia.gemini_service.client.models.generate_content')
    def test_llamar_ahorro_estimado_error_formato_json(self, mock_generate_content):
        # Arrange
        dispositivos = [{"nombre": "Ventilador", "consumo_watts": 50}]
        
        # Stub: Gemini falla y devuelve texto libre en vez de JSON
        mock_response = MagicMock()
        mock_response.text = "Hola, me equivoqué."
        mock_generate_content.return_value = mock_response
        
        # Act
        resultado = llamar_ahorro_estimado(dispositivos)
        
        # Assert: El servicio la captura con JSONDecodeError y devuelve valores por defecto
        assert resultado["ahorro_financiero"] == "No disponible"
        assert resultado["impacto_ambiental"] == "No disponible"
