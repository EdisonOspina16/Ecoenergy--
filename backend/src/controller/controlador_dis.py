import random
import threading
import time
from src.database import obtener_conexion

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
