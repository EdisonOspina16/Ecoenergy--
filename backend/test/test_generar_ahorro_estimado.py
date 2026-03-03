"""
Pruebas unitarias de caja blanca para generar_ahorro_estimado().

La función usa client.models.generate_content() para obtener un JSON de ahorro.
Se mockea esa llamada para cubrir: JSON limpio, JSON con markdown, errores de
parseo, ClientError y excepción genérica.
"""

import json
import pytest
from unittest.mock import Mock, patch

from src.controller import controladorSimulacion as ctrl


# Entrada base común para todos los casos
DISPOSITIVOS_BASE = [{"nombre": "Nevera", "consumo_watts": 150}]


def _mock_response(text: str) -> Mock:
    """Construye un objeto mock con .text para simular la respuesta de generate_content."""
    resp = Mock()
    resp.text = text
    return resp


# -----------------------------------------------------------------------------
# C1 — Respuesta limpia: JSON sin markdown
# -----------------------------------------------------------------------------
def test_generar_ahorro_estimado_c1_respuesta_limpia():
    """
    C1: generate_content() retorna JSON limpio sin markdown.
    Esperado: dict correctamente parseado con ahorro_financiero, impacto_ambiental,
    indicador_didactico.
    """
    json_limpio = json.dumps({
        "ahorro_financiero": "15.000 COP/mes",
        "impacto_ambiental": "8 kg CO₂ menos",
        "indicador_didactico": "Equivale a 3 horas de TV",
    })

    mock_client = Mock()
    mock_client.models.generate_content.return_value = _mock_response(json_limpio)

    with patch("src.controller.controladorSimulacion.client", mock_client):
        resultado = ctrl.generar_ahorro_estimado(DISPOSITIVOS_BASE)

    assert resultado == {
        "ahorro_financiero": "15.000 COP/mes",
        "impacto_ambiental": "8 kg CO₂ menos",
        "indicador_didactico": "Equivale a 3 horas de TV",
    }


# -----------------------------------------------------------------------------
# C2 — Markdown ```json: respuesta envuelta en ```json ... ```
# -----------------------------------------------------------------------------
def test_generar_ahorro_estimado_c2_markdown_json():
    """
    C2: generate_content() retorna texto con bloque ```json\\n{ ... }```.
    El código debe: strip markdown, json.loads, retornar dict OK.
    """
    payload = {
        "ahorro_financiero": "20.000 COP/mes",
        "impacto_ambiental": "12 kg CO₂ menos",
        "indicador_didactico": "Como 4 ciclos de lavadora",
    }
    text_con_markdown = "```json\n" + json.dumps(payload) + "\n```"

    mock_client = Mock()
    mock_client.models.generate_content.return_value = _mock_response(text_con_markdown)

    with patch("src.controller.controladorSimulacion.client", mock_client):
        resultado = ctrl.generar_ahorro_estimado(DISPOSITIVOS_BASE)

    assert resultado == payload


# -----------------------------------------------------------------------------
# C3 — Markdown ``` sin "json": bloque ```\\n{ ... }```
# -----------------------------------------------------------------------------
def test_generar_ahorro_estimado_c3_markdown_sin_json():
    """
    C3: generate_content() retorna ```\\n{ ... }``` (sin etiqueta "json").
    Debe: remover ```, json.loads, retornar dict OK.
    """
    payload = {
        "ahorro_financiero": "10.000 COP/mes",
        "impacto_ambiental": "5 kg CO₂ menos",
        "indicador_didactico": "2 horas menos de AC",
    }
    text_con_markdown = "```\n" + json.dumps(payload) + "\n```"

    mock_client = Mock()
    mock_client.models.generate_content.return_value = _mock_response(text_con_markdown)

    with patch("src.controller.controladorSimulacion.client", mock_client):
        resultado = ctrl.generar_ahorro_estimado(DISPOSITIVOS_BASE)

    assert resultado == payload


# -----------------------------------------------------------------------------
# C4 — JSONDecodeError: texto que no es JSON válido
# -----------------------------------------------------------------------------
def test_generar_ahorro_estimado_c4_json_decode_error():
    """
    C4: generate_content() retorna texto pero JSON malformado.
    Esperado: dict con " No disponible", " No disponible",
    " No fue posible generar la estimación.".
    """
    mock_client = Mock()
    mock_client.models.generate_content.return_value = _mock_response("esto no es json {")

    with patch("src.controller.controladorSimulacion.client", mock_client):
        resultado = ctrl.generar_ahorro_estimado(DISPOSITIVOS_BASE)

    assert resultado == {
        "ahorro_financiero": " No disponible",
        "impacto_ambiental": " No disponible",
        "indicador_didactico": " No fue posible generar la estimación.",
    }


# -----------------------------------------------------------------------------
# C5 — ClientError: la API lanza ClientError
# -----------------------------------------------------------------------------
def test_generar_ahorro_estimado_c5_client_error():
    """
    C5: generate_content() lanza ClientError.
    Esperado: dict con " Error de conexión", " Error de conexión",
    " No fue posible conectar con el servicio de IA.".
    """
    from google.genai.errors import ClientError

    mock_client = Mock()
    mock_client.models.generate_content.side_effect = ClientError("429 Too Many Requests")

    with patch("src.controller.controladorSimulacion.client", mock_client):
        resultado = ctrl.generar_ahorro_estimado(DISPOSITIVOS_BASE)

    assert resultado == {
        "ahorro_financiero": " Error de conexión",
        "impacto_ambiental": " Error de conexión",
        "indicador_didactico": " No fue posible conectar con el servicio de IA.",
    }


# -----------------------------------------------------------------------------
# C6 — Exception: excepción inesperada
# -----------------------------------------------------------------------------
def test_generar_ahorro_estimado_c6_exception():
    """
    C6: generate_content() lanza excepción inesperada (p. ej. RuntimeError).
    Esperado: dict con " Error interno", " Error interno",
    " Ocurrió un error interno al generar la estimación.".
    """
    mock_client = Mock()
    mock_client.models.generate_content.side_effect = RuntimeError("Error inesperado")

    with patch("src.controller.controladorSimulacion.client", mock_client):
        resultado = ctrl.generar_ahorro_estimado(DISPOSITIVOS_BASE)

    assert resultado == {
        "ahorro_financiero": " Error interno",
        "impacto_ambiental": " Error interno",
        "indicador_didactico": " Ocurrió un error interno al generar la estimación.",
    }
