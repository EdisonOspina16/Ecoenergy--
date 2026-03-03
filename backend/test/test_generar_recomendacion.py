"""
Pruebas unitarias de caja blanca para generar_recomendacion().

Ejecuta la API de Gemini a través de client.models.generate_content().
Se mockea esa llamada para cubrir: respuesta exitosa, ClientError y excepción genérica.
"""

import pytest
from unittest.mock import Mock, patch

from src.controller import controladorSimulacion as ctrl


# -----------------------------------------------------------------------------
# C1 — Happy Path: generate_content retorna objeto con .text
# -----------------------------------------------------------------------------
def test_generar_recomendacion_c1_happy_path_respuesta_valida():
    """
    C1 (Happy Path): Entrada consumo_watts=150, dispositivo="Nevera".
    generate_content() retorna objeto con text=" Recomendación válida ".
    Esperado: return response.text.strip() → "Recomendación válida".
    """
    consumo_watts = 150
    dispositivo = "Nevera"

    # Objeto simulado que devuelve la API (con espacios para probar .strip())
    mock_response = Mock()
    mock_response.text = " Recomendación válida "

    mock_client = Mock()
    mock_client.models.generate_content.return_value = mock_response

    with patch("src.controller.controladorSimulacion.client", mock_client):
        resultado = ctrl.generar_recomendacion(consumo_watts, dispositivo)

    assert resultado == "Recomendación válida"
    mock_client.models.generate_content.assert_called_once()
    call_kwargs = mock_client.models.generate_content.call_args[1]
    assert "Nevera" in call_kwargs.get("contents", "")
    assert call_kwargs.get("model") == ctrl.GEMINI_MODEL


# -----------------------------------------------------------------------------
# C2 — ClientError: generate_content lanza ClientError (403, 429, etc.)
# -----------------------------------------------------------------------------
def test_generar_recomendacion_c2_client_error():
    """
    C2 (ClientError): generate_content() lanza ClientError (p. ej. 403 o 429).
    Esperado: return " No fue posible generar la recomendación en este momento. Intenta más tarde."
    """
    from google.genai.errors import ClientError

    mock_client = Mock()
    mock_client.models.generate_content.side_effect = ClientError("API error 403")

    with patch("src.controller.controladorSimulacion.client", mock_client):
        resultado = ctrl.generar_recomendacion(150, "Nevera")

    assert resultado == " No fue posible generar la recomendación en este momento. Intenta más tarde."


# -----------------------------------------------------------------------------
# C3 — Exception: generate_content lanza excepción genérica
# -----------------------------------------------------------------------------
def test_generar_recomendacion_c3_exception_generica():
    """
    C3 (Exception): generate_content() lanza una excepción genérica.
    Esperado: return " Ocurrió un error interno al generar la recomendación."
    """
    mock_client = Mock()
    mock_client.models.generate_content.side_effect = RuntimeError("Error inesperado")

    with patch("src.controller.controladorSimulacion.client", mock_client):
        resultado = ctrl.generar_recomendacion(150, "Nevera")

    assert resultado == " Ocurrió un error interno al generar la recomendación."
