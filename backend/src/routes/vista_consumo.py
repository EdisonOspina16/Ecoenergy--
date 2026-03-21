from functools import wraps
from flask import Blueprint, app, jsonify, request, session
from src.database import obtener_conexion
from src.controller.controladorSimulacion import generar_recomendacion, generar_ahorro_estimado
from src.controller.controladorHogar import obtener_hogar_por_usuario
from src.controller.controladorDispositivos import obtener_dispositivos_por_usuario
from domain.errors import ConexionError

vista_consumo = Blueprint('vista_consumo', __name__)


@app.errorhandler(ConexionError)
def handle_conexion_error(e):
    return jsonify({"success": False, "error": str(e)}), 500

ERROR_DE_CONEXION = "Error de conexión a la base de datos"


def login_requerido(f):
    """Decorador para verificar que el usuario esté autenticado."""
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario = session.get('usuario')
        if not usuario:
            return jsonify({"success": False, "error": "Debes iniciar sesión"}), 401
        return f(*args, **kwargs)
    return decorador

@vista_consumo.route('/home', methods=['GET'])
def consumo_total():
    conn = obtener_conexion()
    if conn is None:
        raise ConexionError(ERROR_DE_CONEXION)

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
        raise ConexionError(ERROR_DE_CONEXION)

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
                    COALESCE(SUM(watts), 0) as consumo
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


@vista_consumo.route('/ahorro-estimado', methods=['GET'])
def ahorro_estimado():
    """
    Calcula el ahorro estimado usando la IA a partir
    de los dispositivos registrados y su último consumo en watts.
    """
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

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

        dispositivos_para_ia = [
            {
                "nombre": row[0] or row[3] or "Dispositivo Sin Nombre",
                "consumo_watts": float(row[1]) if row[1] else 0.0,
            }
            for row in rows
        ]

        cursor.close()
        conn.close()

        if not dispositivos_para_ia:
            return jsonify({
                "success": False,
                "error": "No hay dispositivos registrados para calcular el ahorro"
            }), 400

        resultado = generar_ahorro_estimado(dispositivos_para_ia)

        return jsonify({
            "success": True,
            "data": resultado
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@vista_consumo.route("/recomendacion", methods=["POST"])
def recomendacion():
    data = request.get_json()
    consumo = data.get("consumo_watts")
    dispositivo = data.get("dispositivo")
    
    resultado = generar_recomendacion(consumo, dispositivo)
    
    # Detectar el tipo de recomendación
    es_alerta = any(palabra in resultado.lower() for palabra in ['⚠️', 'pico', 'anómalo', 'inusual', 'alerta'])
    
    return jsonify({
        "recomendacion": resultado,
        "esAlerta": es_alerta,
        "dispositivo": dispositivo
    })


# ---- Recomendación y ahorro diario (una vez por usuario por día) ----

@vista_consumo.route("/recomendacion-diaria", methods=["GET"])
@login_requerido
def obtener_recomendacion_diaria():
    """
    Devuelve la recomendación y ahorro estimado del día para el hogar del usuario.
    Si no hay registro para hoy, devuelve vacío (el front puede pedir generar con POST).
    """
    try:
        usuario = session.get("usuario")
        id_usuario = usuario["id"]
        hogar = obtener_hogar_por_usuario(id_usuario)
        if not hogar:
            return jsonify({
                "success": True,
                "recomendaciones": [],
                "ahorro_financiero": None,
                "impacto_ambiental": None,
                "indicador_didactico": None,
            })

        conn = obtener_conexion()
        if not conn:
            raise ConexionError(ERROR_DE_CONEXION)

        cur = conn.cursor()
        cur.execute(
            """
            SELECT recomendaciones, ahorro_financiero, impacto_ambiental, indicador_didactico
            FROM recomendacion_ahorro_diaria
            WHERE id_hogar = %s AND fecha = CURRENT_DATE
            """,
            (hogar.id_hogar,),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return jsonify({
                "success": True,
                "recomendaciones": [],
                "ahorro_financiero": None,
                "impacto_ambiental": None,
                "indicador_didactico": None,
            })

        import json as _json
        recs = row[0] if row[0] is not None else []
        if isinstance(recs, str):
            recs = _json.loads(recs) if recs else []

        return jsonify({
            "success": True,
            "recomendaciones": recs,
            "ahorro_financiero": row[1],
            "impacto_ambiental": row[2],
            "indicador_didactico": row[3],
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@vista_consumo.route("/recomendacion-diaria/generar", methods=["POST"])
@login_requerido
def generar_recomendacion_diaria():
    """
    Genera recomendación y ahorro estimado para hoy y los guarda.
    Si ya existe registro para hoy, devuelve el guardado sin volver a llamar a la IA.
    """
    try:
        usuario = session.get("usuario")
        id_usuario = usuario["id"]
        hogar = obtener_hogar_por_usuario(id_usuario)
        if not hogar:
            return jsonify({"success": False, "error": "No tienes un hogar registrado"}), 400

        conn = obtener_conexion()
        if not conn:
            raise ConexionError(ERROR_DE_CONEXION)

        cur = conn.cursor()

        # Si ya hay registro para hoy, devolverlo
        cur.execute(
            """
            SELECT recomendaciones, ahorro_financiero, impacto_ambiental, indicador_didactico
            FROM recomendacion_ahorro_diaria
            WHERE id_hogar = %s AND fecha = CURRENT_DATE
            """,
            (hogar.id_hogar,),
        )
        row = cur.fetchone()
        if row:
            import json as _json
            recs = row[0] if row[0] is not None else []
            if isinstance(recs, str):
                recs = _json.loads(recs) if recs else []
            cur.close()
            conn.close()
            return jsonify({
                "success": True,
                "recomendaciones": recs,
                "ahorro_financiero": row[1],
                "impacto_ambiental": row[2],
                "indicador_didactico": row[3],
            })

        # Obtener dispositivos del hogar del usuario con último consumo (watts)
        cur.execute(
            """
            SELECT DISTINCT ON (d.id_dispositivos)
                COALESCE(d.alias, d.tipo_dispositivo_ia, 'Dispositivo') AS nombre,
                COALESCE(r.watts, 0)::float AS watts
            FROM dispositivos d
            INNER JOIN hogares h ON d.id_hogar = h.id_hogar
            LEFT JOIN registros_consumo r ON r.id_dispositivo = d.id_dispositivos
            WHERE h.id_usuario = %s
            ORDER BY d.id_dispositivos, r.fecha_hora DESC NULLS LAST
            """,
            (id_usuario,),
        )
        dispositivos_rows = cur.fetchall()
        cur.close()
        conn.close()

        dispositivos_para_ia = [{"nombre": r[0], "consumo_watts": r[1] or 0} for r in dispositivos_rows]
        if not dispositivos_para_ia:
            return jsonify({
                "success": False,
                "error": "No hay dispositivos registrados para generar la recomendación"
            }), 400

        # Generar recomendación por dispositivo
        recomendaciones_list = []
        for d in dispositivos_para_ia:
            texto = generar_recomendacion(d["consumo_watts"], d["nombre"])
            es_alerta = any(
                p in texto.lower() for p in ["⚠️", "pico", "anómalo", "inusual", "alerta"]
            )
            recomendaciones_list.append({
                "recomendacion": texto,
                "esAlerta": es_alerta,
                "dispositivo": d["nombre"],
            })

        # Generar ahorro estimado
        ahorro = generar_ahorro_estimado(dispositivos_para_ia)

        # Guardar en BD
        import json as _json
        conn = obtener_conexion()
        if not conn:
            raise ConexionError(ERROR_DE_CONEXION)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO recomendacion_ahorro_diaria
                (id_hogar, fecha, recomendaciones, ahorro_financiero, impacto_ambiental, indicador_didactico)
            VALUES (%s, CURRENT_DATE, %s::jsonb, %s, %s, %s)
            ON CONFLICT (id_hogar, fecha) DO NOTHING
            """,
            (
                hogar.id_hogar,
                _json.dumps(recomendaciones_list),
                ahorro.get("ahorro_financiero"),
                ahorro.get("impacto_ambiental"),
                ahorro.get("indicador_didactico"),
            ),
        )
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "recomendaciones": recomendaciones_list,
            "ahorro_financiero": ahorro.get("ahorro_financiero"),
            "impacto_ambiental": ahorro.get("impacto_ambiental"),
            "indicador_didactico": ahorro.get("indicador_didactico"),
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
