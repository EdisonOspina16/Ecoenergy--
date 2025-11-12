import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from src.database import obtener_conexion

def guardar_indicador(indicador):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        query = """
        INSERT INTO indicadores (usuario_id, energia_ahorrada_kwh, reduccion_co2_kg,
                                 arboles_salvados, ahorro_economico, periodo, fecha_creacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id_indicador;
        """
        cursor.execute(query, (
            indicador.usuario_id,
            indicador.energia_ahorrada_kwh,
            indicador.reduccion_co2_kg,
            indicador.arboles_salvados,
            indicador.ahorro_economico,
            indicador.periodo,
            indicador.fecha_creacion
        ))
        new_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return new_id
    except Exception as e:
        print(f"Error guardando indicador: {e}")
        return None


def obtener_indicadores_por_usuario(usuario_id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        query = """
        SELECT id_indicador, usuario_id, energia_ahorrada_kwh, reduccion_co2_kg,
               arboles_salvados, ahorro_economico, periodo, fecha_creacion
        FROM indicadores
        WHERE usuario_id = %s
        ORDER BY fecha_creacion DESC;
        """
        cursor.execute(query, (usuario_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        indicadores = []
        for r in rows:
            indicadores.append({
                "id_indicador": r[0],
                "usuario_id": r[1],
                "energia_ahorrada_kwh": float(r[2]),
                "reduccion_co2_kg": float(r[3]),
                "arboles_salvados": float(r[4]),
                "ahorro_economico": float(r[5]),
                "periodo": str(r[6]),
                "fecha_creacion": str(r[7])
            })
        return indicadores
    except Exception as e:
        print(f"Error obteniendo indicadores: {e}")
        return []
