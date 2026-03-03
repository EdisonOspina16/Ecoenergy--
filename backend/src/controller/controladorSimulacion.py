import random
import threading
import time
import json
from src.database import obtener_conexion
from src.SecretConfig import GEMINI_API_KEY, GEMINI_MODEL
from google.genai.errors import ClientError
from google import genai

# IDs de los dispositivos (ajústalos a los que tengas en tu tabla 'dispositivos')
DISPOSITIVOS = {
    "televisor": 1,
    "nevera": 2,
    "aire_acondicionado": 3
}

# Rango de consumo realista en kWh cada 5 segundos
RANGOS_CONSUMO = {
    "televisor": (0.000167, 0.000433),
    "nevera": (0.000417, 0.001),
    "aire_acondicionado": (0.002083, 0.005167)
}

def simular_consumo():
    """
    Simula el consumo de energía de tres dispositivos y guarda los valores en la base de datos.
    """
    conn = obtener_conexion()
    if conn is None:
        print(" No se pudo conectar a la base de datos.")
        return

    try:
        while True:
            with conn.cursor() as cursor:
                for nombre, id_disp in DISPOSITIVOS.items():
                    min_kwh, max_kwh = RANGOS_CONSUMO[nombre]
                    consumo_kwh = round(random.uniform(min_kwh, max_kwh), 6)
                    
                    # Simular valores eléctricos coherentes
                    voltage = round(random.uniform(110, 120), 2)  # voltaje típico
                    current = round(random.uniform(0.2, 5.0), 2)  # corriente variable
                    watts = round(voltage * current, 2)

                    cursor.execute("""
                        INSERT INTO registros_consumo (id_dispositivo, consumo_kwh, fecha_hora, watts, voltage, current)
                        VALUES (%s, %s, NOW(), %s, %s, %s);
                    """, (id_disp, consumo_kwh, watts, voltage, current))

            conn.commit()
            print(" Datos insertados correctamente en registros_consumo.")
            time.sleep(5) 

    except Exception as e:
        print(f" Error en la simulación: {e}")
    finally:
        conn.close()

def iniciar_simulacion(): 
    """
    Inicia la simulación en un hilo separado para no bloquear Flask.
    """
    hilo = threading.Thread(target=simular_consumo, daemon=True)
    hilo.start()
    print(" Simulación de consumo iniciada.") 


#----google gemini----#

client = genai.Client(
    api_key=GEMINI_API_KEY
)

GEMINI_MODEL = GEMINI_MODEL

def generar_recomendacion(consumo_watts, dispositivo):
    """
    Genera una recomendación de consumo energético usando la API de Gemini.
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
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return response.text.strip()

    except ClientError as e:
        # Error de API (403, 401, 429, etc.)
        print(f"Error Gemini: {e}")
        return " No fue posible generar la recomendación en este momento. Intenta más tarde."

    except Exception as e:
        # Cualquier otro error inesperado
        print(f"Error inesperado: {e}")
        return " Ocurrió un error interno al generar la recomendación."
    

def generar_ahorro_estimado(dispositivos: list[dict]) -> dict:
    """
    Genera estimación de ahorro financiero, impacto ambiental e indicador didáctico
    a partir de una lista de dispositivos y su consumo.

    Args:
        dispositivos: Lista de dicts con keys 'nombre' y 'consumo_watts'
                      Ejemplo: [{"nombre": "Aire acondicionado", "consumo_watts": 1500},
                                {"nombre": "Nevera", "consumo_watts": 200}]

    Returns:
        dict con keys:
            - ahorro_financiero: str  → "25.000 COP/mes"
            - impacto_ambiental: str  → "10 kg CO₂ menos"
            - indicador_didactico: str → "Equivale a 5 horas menos de AC"
    """

    resumen_dispositivos = "\n".join(
        [f"- {d['nombre']}: {d['consumo_watts']} W" for d in dispositivos]
    )
    consumo_total = sum(d['consumo_watts'] for d in dispositivos)

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
{resumen_dispositivos}

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
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "temperature": 0.9,
                "top_p": 0.95,
            }
        )

        raw = response.text.strip()

        # Limpiar posibles bloques markdown si Gemini los incluye
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
        print(f"Error parseando JSON de Gemini: {e}\nRespuesta raw: {raw}")
        return {
            "ahorro_financiero": " No disponible",
            "impacto_ambiental": " No disponible",
            "indicador_didactico": " No fue posible generar la estimación.",
        }

    except ClientError as e:
        print(f"Error Gemini API: {e}")
        return {
            "ahorro_financiero": " Error de conexión",
            "impacto_ambiental": " Error de conexión",
            "indicador_didactico": " No fue posible conectar con el servicio de IA.",
        }

    except Exception as e:
        print(f"Error inesperado: {e}")
        return {
            "ahorro_financiero": " Error interno",
            "impacto_ambiental": " Error interno",
            "indicador_didactico": " Ocurrió un error interno al generar la estimación.",
        }