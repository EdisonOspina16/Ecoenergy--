import json
from google.genai.errors import ClientError
from src.infrastructure.ia.gemini_client import client, MODELO
from src.infrastructure.ia.gemini_helpers import (
    construir_prompt_recomendacion,
    construir_prompt_ahorro_estimado,
    parsear_respuesta_gemini,
    fallback_por_excepcion,
)


def llamar_recomendacion(consumo_watts: float, dispositivo: str) -> str:
    """
    Llama a la API de Gemini y retorna el texto de recomendación
    para un dispositivo con su consumo en watts.
    """
    prompt = construir_prompt_recomendacion(consumo_watts, dispositivo)
    try:
        response = client.models.generate_content(model=MODELO, contents=prompt)
        return response.text.strip()
    except ClientError as e:
        print(f"[Gemini] ClientError en recomendacion: {e}")
        return "No fue posible generar la recomendación en este momento. Intenta más tarde."
    except Exception as e:
        print(f"[Gemini] Error inesperado en recomendacion: {e}")
        return "Ocurrió un error interno al generar la recomendación."


def llamar_ahorro_estimado(dispositivos: list[dict]) -> dict:
    """
    Llama a la API de Gemini y retorna un dict con:
    - ahorro_financiero
    - impacto_ambiental
    - indicador_didactico

    Recibe una lista de dicts con keys 'nombre' y 'consumo_watts'.
    """
    prompt = construir_prompt_ahorro_estimado(dispositivos)

    try:
        response = client.models.generate_content(
            model=MODELO,
            contents=prompt,
            config={"temperature": 0.9, "top_p": 0.95},
        )
        return parsear_respuesta_gemini(response.text.strip())

    except json.JSONDecodeError as e:
        print(f"[Gemini] Error JSON: {e}")
        return fallback_por_excepcion(e)

    except ClientError as e:
        print(f"[Gemini] Error API Gemini: {e}")
        return fallback_por_excepcion(e)

    except Exception as e:
        print(f"[Gemini] Error inesperado: {e}")
        return fallback_por_excepcion(e)