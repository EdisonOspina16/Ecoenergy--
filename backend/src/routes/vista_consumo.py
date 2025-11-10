from flask import Blueprint, jsonify
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
            SELECT COALESCE(SUM(consumo_kwh), 0)
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
