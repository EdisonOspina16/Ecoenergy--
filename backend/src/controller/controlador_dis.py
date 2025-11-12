import random
import threading
import time
from src.database import obtener_conexion
from src.SecretConfig import GEMINI_API_KEY, GEMINI_MODEL
from google import genai

# IDs de los dispositivos (ajústalos a los que tengas en tu tabla 'dispositivos')
DISPOSITIVOS = {
    "televisor": 1,
    "nevera": 2,
    "aire_acondicionado": 3
}

# Rango de consumo realista en kWh cada 5 segundos
RANGOS_CONSUMO = {
    "televisor": (0.00002, 0.00005),
    "nevera": (0.00005, 0.00015),
    "aire_acondicionado": (0.00015, 0.00030)
}

def simular_consumo():
    """
    Simula el consumo de energía de tres dispositivos y guarda los valores en la base de datos.
    """
    conn = obtener_conexion()
    if conn is None:
        print("❌ No se pudo conectar a la base de datos.")
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
            print("✅ Datos insertados correctamente en registros_consumo.")
            time.sleep(5)

    except Exception as e:
        print(f"⚠️ Error en la simulación: {e}")
    finally:
        conn.close()

def iniciar_simulacion():
    """
    Inicia la simulación en un hilo separado para no bloquear Flask.
    """
    hilo = threading.Thread(target=simular_consumo, daemon=True)
    hilo.start()
    print("🚀 Simulación de consumo iniciada.")


#----google gemini----#
def generar_recomendacion(consumo_watts, dispositivo):
    """
    Genera una recomendación de consumo energético usando la API de Gemini.
    """
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Combinas el prompt base con los datos del usuario
    prompt = f"""
    Eres un asistente energético inteligente especializado en analizar el consumo de dispositivos eléctricos en hogares y empresas.

    Analiza los siguientes datos del usuario:
    - Dispositivo: {dispositivo}
    - Consumo detectado: {consumo_watts} W


    Tu objetivo es generar una recomendación útil, clara y amigable. 
    Sigue estas reglas al responder:

    1️⃣ **Si el consumo es anormalmente alto**
    - Muestra una alerta con tono preventivo y un ícono de advertencia (⚠️).
    - Ejemplo: "⚠️ Pico de consumo detectado: el {dispositivo} está usando más energía de la habitual. Revisa si quedó encendido por error o si requiere mantenimiento."

    2️⃣ **Si el consumo supera el promedio histórico estimado del dispositivo**
    - Muestra una recomendación en tono informativo con un ícono verde (💡).
    - Ejemplo: "💡 Tu {dispositivo} consume un 25% más de lo normal. Verifica la configuración o intenta usarlo en horarios de menor demanda."

    3️⃣ **Si el consumo es estable y normal**
    - Devuelve un mensaje corto y positivo con un ícono verde (✅).
    - Ejemplo: "✅ El consumo del {dispositivo} está dentro de los rangos esperados. ¡Buen uso energético!"

    4️⃣ **Si el consumo es muy bajo o irregular**
    - Sugiere posibles causas o ahorro.
    - Ejemplo: "🌙 El {dispositivo} está usando poca energía a esta hora. Podrías aprovechar para desconectarlo si no lo necesitas."

    Responde **solo con el texto final de la recomendación**, sin incluir explicaciones, formato JSON ni información adicional.
    """

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text.strip()
