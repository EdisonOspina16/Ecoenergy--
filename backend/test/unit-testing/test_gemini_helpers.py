import pytest
import json
from google.genai.errors import ClientError
from hamcrest import assert_that, is_, contains_string, equal_to

from src.infrastructure.ia.gemini_helpers import (
    construir_prompt_recomendacion,
    construir_prompt_ahorro_estimado,
    _limpiar_markdown,
    _extraer_recomendaciones,
    parsear_respuesta_gemini,
    fallback_por_excepcion,
)

class TestGeminiHelpers:

    def test_construir_prompt_recomendacion_incluye_datos(self):
        # Arrange
        consumo = 150.0
        dispositivo = "Lavadora"

        # Act
        resultado = construir_prompt_recomendacion(consumo, dispositivo)

        # Assert
        assert_that(resultado, contains_string("Lavadora"))
        assert_that(resultado, contains_string("150.0 W"))
        assert_that(resultado, contains_string("Reglas:"))

    def test_construir_prompt_ahorro_estimado_incluye_datos(self):
        # Arrange
        dispositivos = [{"nombre": "Nevera", "consumo_watts": 400}]

        # Act
        resultado = construir_prompt_ahorro_estimado(dispositivos)

        # Assert
        assert_that(resultado, contains_string("Nevera: 400 W"))
        assert_that(resultado, contains_string("Consumo total estimado: 400 W"))
        assert_that(resultado, contains_string("ahorro_financiero"))

    def test_limpiar_markdown_sin_etiquetas_retorna_igual(self):
        # Arrange
        texto_crudo = '{"clave": "valor"}'

        # Act
        resultado = _limpiar_markdown(texto_crudo)

        # Assert
        assert_that(resultado, is_(equal_to('{"clave": "valor"}')))

    def test_limpiar_markdown_con_etiqueta_json_retorna_limpio(self):
        # Arrange
        texto_crudo = '```json\n{"clave": "valor"}\n```'

        # Act
        resultado = _limpiar_markdown(texto_crudo)

        # Assert
        assert_that(resultado, is_(equal_to('{"clave": "valor"}')))

    def test_limpiar_markdown_con_etiqueta_simple_retorna_limpio(self):
        # Arrange
        texto_crudo = '```\n{"clave": "valor"}\n```'

        # Act
        resultado = _limpiar_markdown(texto_crudo)

        # Assert
        assert_that(resultado, is_(equal_to('{"clave": "valor"}')))

    def test_extraer_recomendaciones_completas_retorna_todas(self):
        # Arrange
        datos = {
            "ahorro_financiero": "1000",
            "impacto_ambiental": "2kg",
            "indicador_didactico": "1 hora",
            "otra_clave": "ignorar"
        }

        # Act
        resultado = _extraer_recomendaciones(datos)

        # Assert
        assert_that(resultado, is_(equal_to({
            "ahorro_financiero": "1000",
            "impacto_ambiental": "2kg",
            "indicador_didactico": "1 hora",
        })))

    def test_extraer_recomendaciones_incompletas_aplica_na(self):
        # Arrange
        datos = {"ahorro_financiero": "1000"}

        # Act
        resultado = _extraer_recomendaciones(datos)

        # Assert
        assert_that(resultado, is_(equal_to({
            "ahorro_financiero": "1000",
            "impacto_ambiental": "N/A",
            "indicador_didactico": "N/A",
        })))

    def test_parsear_respuesta_gemini_valida_retorna_dict(self):
        # Arrange
        texto = '```json\n{"ahorro_financiero": "100", "impacto_ambiental": "1", "indicador_didactico": "2"}\n```'

        # Act
        resultado = parsear_respuesta_gemini(texto)

        # Assert
        assert_that(resultado["ahorro_financiero"], is_(equal_to("100")))
        assert_that(resultado["impacto_ambiental"], is_(equal_to("1")))

    def test_fallback_por_excepcion_json_decode_error(self):
        # Arrange
        error = json.JSONDecodeError("msg", "doc", 0)

        # Act
        resultado = fallback_por_excepcion(error)

        # Assert
        assert_that(resultado["ahorro_financiero"], is_(equal_to("No disponible")))
        assert_that(resultado["indicador_didactico"], contains_string("No fue posible generar"))

    def test_fallback_por_excepcion_client_error(self):
        # Arrange
        error = ClientError("msg", 400)

        # Act
        resultado = fallback_por_excepcion(error)

        # Assert
        assert_that(resultado["ahorro_financiero"], is_(equal_to("Error de conexión")))
        assert_that(resultado["indicador_didactico"], contains_string("servicio de IA"))

    def test_fallback_por_excepcion_generica(self):
        # Arrange
        error = ValueError("Cualquier cosa")

        # Act
        resultado = fallback_por_excepcion(error)

        # Assert
        assert_that(resultado["ahorro_financiero"], is_(equal_to("Error interno")))
        assert_that(resultado["indicador_didactico"], contains_string("error interno"))
