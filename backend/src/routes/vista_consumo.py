from flask import Blueprint, jsonify, request
from src.database import obtener_conexion

vista_consumo = Blueprint('vista_consumo', __name__)

@vista_consumo.route('/home', methods=['GET'])
def consumo_total():
    conn = obtener_conexion()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cur = conn.cursor()
        # Consulta suma consumo últimos 1 día
        cur.execute("""
            SELECT COALESCE(SUM(watts), 0)
            FROM registros_consumo
            WHERE fecha_hora >= NOW() - INTERVAL '1 day';
        """)
        resultado = cur.fetchone()
        total_consumo = resultado[0] if resultado else 0

        cur.close()
        conn.close()

        return jsonify({"total_consumo_kwh": float(total_consumo)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@vista_consumo.route('/consumo-historico', methods=['GET'])
def consumo_historico():
    """
    Endpoint para obtener datos históricos de consumo
    Query params: rango = 'day' | 'week' | 'month'
    """
    conn = obtener_conexion()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        rango = request.args.get('rango', 'day')
        cur = conn.cursor()
        
        if rango == 'day':
            # Consumo por hora en las últimas 24 horas
            cur.execute("""
                SELECT 
                    TO_CHAR(fecha_hora, 'HH24:00') as periodo,
                    COALESCE(SUM(watts), 0) as consumo
                FROM registros_consumo
                WHERE fecha_hora >= NOW() - INTERVAL '1 day'
                GROUP BY TO_CHAR(fecha_hora, 'HH24:00'), DATE_TRUNC('hour', fecha_hora)
                ORDER BY DATE_TRUNC('hour', fecha_hora);
            """)
            
        elif rango == 'week':
            # Consumo por día en los últimos 7 días
            cur.execute("""
                SELECT 
                    TO_CHAR(fecha_hora, 'Dy DD') as periodo,
                    COALESCE(SUM(watts), 0) as consumo
                FROM registros_consumo
                WHERE fecha_hora >= NOW() - INTERVAL '7 days'
                GROUP BY TO_CHAR(fecha_hora, 'Dy DD'), DATE_TRUNC('day', fecha_hora)
                ORDER BY DATE_TRUNC('day', fecha_hora);
            """)
            
        else:  # month
            # Consumo por día en los últimos 30 días
            cur.execute("""
                SELECT 
                    TO_CHAR(fecha_hora, 'DD/MM') as periodo,
                    COALESCE(SUM(watts, 0) as consumo
                FROM registros_consumo
                WHERE fecha_hora >= NOW() - INTERVAL '30 days'
                GROUP BY TO_CHAR(fecha_hora, 'DD/MM'), DATE_TRUNC('day', fecha_hora)
                ORDER BY DATE_TRUNC('day', fecha_hora);
            """)
        
        resultados = cur.fetchall()
        
        # Formatear datos para el frontend
        datos = [
            {
                "periodo": row[0],
                "consumo": float(row[1])
            }
            for row in resultados
        ]
        
        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "rango": rango,
            "datos": datos
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
@vista_consumo.route('/dispositivos', methods=['GET'])
def obtener_dispositivos():
    """
    Devuelve la lista de dispositivos con su consumo individual
    """
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Dispositivos con su último registro
        cursor.execute("""
            SELECT DISTINCT ON (d.id_dispositivos)
                d.alias,
                r.watts,
                d.estado_activo,
                d.tipo_dispositivo_ia
            FROM dispositivos AS d
            LEFT JOIN registros_consumo AS r 
                ON r.id_dispositivo = d.id_dispositivos
            ORDER BY d.id_dispositivos, r.fecha_hora DESC
        """)

        rows = cursor.fetchall()
        dispositivos = [
            {
                "nombre": row[0] or row[3] or "Dispositivo Sin Nombre",
                "consumo": float(row[1]) / 1000 if row[1] else 0.0,
                "estado": "Encendido" if row[2] else "Apagado",
                "watts": float(row[1]) if row[1] else 0.0
            }
            for row in rows
        ]

        cursor.close()
        conn.close()

        return jsonify({
            "success": True, 
            "dispositivos": dispositivos
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500