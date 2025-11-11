"""
Script para insertar datos de prueba en la base de datos
para verificar las gráficas de consumo histórico
"""

import psycopg2
from datetime import datetime, timedelta
import random

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ecoenergy',  # Cambia esto
    'user': 'postgres',            # Cambia esto
    'password': 'Luciana-0313'        # Cambia esto
}

def obtener_conexion():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error al conectar: {e}")
        return None

def insertar_datos_prueba():
    conn = obtener_conexion()
    if conn is None:
        print("No se pudo conectar a la base de datos")
        return
    
    cur = conn.cursor()
    
    # Dispositivos según tu tabla
    dispositivos = [
        {'id': 1, 'nombre': 'Televisor Sala', 'consumo_base': 0.15},
        {'id': 2, 'nombre': 'Nevera', 'consumo_base': 0.80},
        {'id': 3, 'nombre': 'Aire Acondicionado', 'consumo_base': 1.5}
    ]
    
    print("Insertando datos históricos...")
    
    # Generar datos para los últimos 30 días
    fecha_inicio = datetime.now() - timedelta(days=30)
    registros_insertados = 0
    
    for dia in range(31):
        fecha_dia = fecha_inicio + timedelta(days=dia)
        
        # Generar 24 registros por día (uno por hora)
        for hora in range(24):
            fecha_hora = fecha_dia.replace(hour=hora, minute=0, second=0, microsecond=0)
            
            for dispositivo in dispositivos:
                # Simular variaciones de consumo
                variacion = random.uniform(0.8, 1.3)
                consumo = dispositivo['consumo_base'] * variacion
                
                # El AC solo consume en horas de calor (10am - 10pm)
                if dispositivo['id'] == 3 and (hora < 10 or hora > 22):
                    consumo = 0
                
                # La nevera consume constante pero con ligeras variaciones
                if dispositivo['id'] == 2:
                    consumo = dispositivo['consumo_base'] * random.uniform(0.95, 1.05)
                
                # El TV consume más en horas nocturnas (6pm - 11pm)
                if dispositivo['id'] == 1:
                    if 18 <= hora <= 23:
                        consumo = dispositivo['consumo_base'] * random.uniform(1.0, 1.5)
                    else:
                        consumo = dispositivo['consumo_base'] * random.uniform(0.2, 0.8)
                
                watts = consumo * 1000  # Convertir kWh a watts
                
                try:
                    cur.execute("""
                        INSERT INTO registros_consumo 
                        (id_dispositivo_iot, fecha_hora, watts, consumo_kwh)
                        VALUES (%s, %s, %s, %s)
                    """, (dispositivo['id'], fecha_hora, watts, consumo))
                    registros_insertados += 1
                    
                except Exception as e:
                    print(f"Error insertando registro: {e}")
                    continue
    
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"✓ Se insertaron {registros_insertados} registros de prueba")
    print(f"✓ Rango de fechas: {fecha_inicio.strftime('%Y-%m-%d')} a {datetime.now().strftime('%Y-%m-%d')}")
    print("\nPuedes probar ahora:")
    print("- Vista por día: últimas 24 horas")
    print("- Vista por semana: últimos 7 días")
    print("- Vista por mes: últimos 30 días")

def verificar_datos():
    """Verifica cuántos registros hay en la base de datos"""
    conn = obtener_conexion()
    if conn is None:
        return
    
    cur = conn.cursor()
    
    # Total de registros
    cur.execute("SELECT COUNT(*) FROM registros_consumo")
    total = cur.fetchone()[0]
    print(f"\nTotal de registros: {total}")
    
    # Registros por dispositivo
    cur.execute("""
        SELECT d.alias, COUNT(*) 
        FROM registros_consumo r
        JOIN dispositivos_iot d ON r.id_dispositivo_iot = d.id_dispositivos
        GROUP BY d.alias
    """)
    print("\nRegistros por dispositivo:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]} registros")
    
    # Rango de fechas
    cur.execute("""
        SELECT MIN(fecha_hora), MAX(fecha_hora) 
        FROM registros_consumo
    """)
    rango = cur.fetchone()
    if rango[0]:
        print(f"\nRango de fechas: {rango[0]} a {rango[1]}")
    
    cur.close()
    conn.close()

def limpiar_datos_prueba():
    """Elimina todos los registros de prueba"""
    respuesta = input("\n¿Estás seguro de que quieres eliminar todos los registros? (s/n): ")
    if respuesta.lower() != 's':
        print("Operación cancelada")
        return
    
    conn = obtener_conexion()
    if conn is None:
        return
    
    cur = conn.cursor()
    cur.execute("DELETE FROM registros_consumo")
    registros_eliminados = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"✓ Se eliminaron {registros_eliminados} registros")

if __name__ == "__main__":
    print("=== Script de Prueba - Datos Históricos ===\n")
    print("1. Insertar datos de prueba")
    print("2. Verificar datos existentes")
    print("3. Limpiar datos de prueba")
    print("4. Salir")
    
    opcion = input("\nSelecciona una opción: ")
    
    if opcion == "1":
        insertar_datos_prueba()
    elif opcion == "2":
        verificar_datos()
    elif opcion == "3":
        limpiar_datos_prueba()
    else:
        print("Saliendo...")