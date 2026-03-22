import json
import random
from google.genai.errors import ClientError
from src.infrastructure.ia.gemini_client import client, MODELO


def llamar_recomendacion(consumo_watts: float, dispositivo: str) -> str:
    """
    Llama a la API de Gemini y retorna el texto de recomendación
    para un dispositivo con su consumo en watts.
    """
    prompt = f"""
    Eres un asistente energético inteligente especializado en analizar el consumo de dispositivos eléctricos.

    Datos del usuario:
    - Dispositivo: {dispositivo}
    - Consumo detectado: {consumo_watts} W

    Reglas:
    1️⃣ Consumo alto → alerta ⚠️
    2️⃣ Consumo superior al promedio → recomendación 💡
    3️⃣ Consumo normal → mensaje positivo ✅
    4️⃣ Consumo bajo o irregular → sugerencia 🌙

    Responde solo con el texto final de la recomendación.
    """
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
    resumen = "\n".join(
        [f"- {d['nombre']}: {d['consumo_watts']} W" for d in dispositivos]
    )
    consumo_total = sum(d["consumo_watts"] for d in dispositivos)

    estilos_didacticos = [
        "Usa una analogía con electrodomésticos del hogar (ej: horas de televisor, ciclos de lavadora).",
        "Usa una analogía con actividades cotidianas y tiempo (ej: horas de trabajo, viajes en bus).",
        "Usa una analogía con naturaleza o medio ambiente (ej: árboles plantados, litros de agua ahorrados).",
        "Usa una analogía con dinero o compras del día a día (ej: paquetes de arroz, recargas de celular).",
        "Usa una analogía con comida o cocina (ej: horas de horno encendido, tazas de café preparadas).",
    ]

    estilo_aleatorio = random.choice(estilos_didacticos)
    variacion = random.randint(1, 9999)

    prompt = f"""
Eres un asistente energético inteligente especializado en analizar el consumo de dispositivos eléctricos en Colombia.

El usuario tiene los siguientes dispositivos en su hogar:
{resumen}

Consumo total estimado: {consumo_total} W

Tu tarea es generar UNA estimación de ahorro si el usuario aplica buenas prácticas de eficiencia energética (reducir uso un 20-30%).

Debes responder ÚNICAMENTE con un JSON válido con exactamente estas 3 claves, sin texto adicional, sin markdown, sin explicaciones:

{{
  "ahorro_financiero": "<monto en COP por mes, ej: 5.000 COP/mes>",
  "impacto_ambiental": "<kg de CO2 reducidos, ej: 10 kg CO₂ menos>",
  "indicador_didactico": "<analogía cotidiana creativa y corta>"
}}

Reglas:
- Usa la tarifa promedio de energía en Colombia: ~800 COP por kWh
- Calcula el CO₂ con el factor colombiano: ~0.126 kg CO₂ por kWh
- {estilo_aleatorio}
- El indicador didáctico debe ser corto, máximo 10 palabras, fácil de entender para cualquier persona
- Los valores deben ser realistas y coherentes con el consumo indicado
- Sé original y creativo, no repitas analogías comunes
- Responde SOLO el JSON, nada más
[Variación #{variacion}]
"""
    try:
        response = client.models.generate_content(
            model=MODELO,
            contents=prompt,
            config={"temperature": 0.9, "top_p": 0.95},
        )
        raw = response.text.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        resultado = json.loads(raw)
        return {
            "ahorro_financiero": resultado.get("ahorro_financiero", "N/A"),
            "impacto_ambiental": resultado.get("impacto_ambiental", "N/A"),
            "indicador_didactico": resultado.get("indicador_didactico", "N/A"),
        }

    except json.JSONDecodeError as e:
        print(f"[Gemini] JSONDecodeError en ahorro: {e}")
        return {
            "ahorro_financiero": "No disponible",
            "impacto_ambiental": "No disponible",
            "indicador_didactico": "No fue posible generar la estimación.",
        }
    except ClientError as e:
        print(f"[Gemini] ClientError en ahorro: {e}")
        return {
            "ahorro_financiero": "Error de conexión",
            "impacto_ambiental": "Error de conexión",
            "indicador_didactico": "No fue posible conectar con el servicio de IA.",
        }
    except Exception as e:
        print(f"[Gemini] Error inesperado en ahorro: {e}")
        return {
            "ahorro_financiero": "Error interno",
            "impacto_ambiental": "Error interno",
            "indicador_didactico": "Ocurrió un error interno al generar la estimación.",
        }
    