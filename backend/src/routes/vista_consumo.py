from flask import Blueprint, jsonify, request, session
from src.aplication.service.consumo_service import (
    procesar_recomendacion,
    procesar_ahorro_estimado,
    obtener_recomendacion_diaria_hogar_por_usuario,
    generar_y_guardar_recomendacion_diaria,
)
from src.repositories.usuario_repository import UsuarioRepository
from src.routes.vista_usuarios import login_requerido


vista_consumo = Blueprint("vista_consumo", __name__)


@vista_consumo.route("/ahorro-estimado", methods=["GET"])
def ahorro_estimado():
    try:
        resultado = procesar_ahorro_estimado()
        return jsonify({"success": True, "data": resultado})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@vista_consumo.route("/recomendacion", methods=["POST"])
def recomendacion():
    try:
        data = request.get_json()
        consumo = data.get("consumo_watts")
        dispositivo = data.get("dispositivo")
        resultado = procesar_recomendacion(consumo, dispositivo)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@vista_consumo.route("/recomendacion-diaria", methods=["GET"])
@login_requerido
def obtener_recomendacion_diaria():
    try:
        usuario = session.get("usuario")
        resultado = obtener_recomendacion_diaria_hogar_por_usuario(usuario["id"])
        return jsonify({"success": True, **resultado})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@vista_consumo.route("/recomendacion-diaria/generar", methods=["POST"])
@login_requerido
def generar_recomendacion_diaria():
    try:
        usuario = session.get("usuario")
        resultado = generar_y_guardar_recomendacion_diaria(usuario["id"])
        return jsonify({"success": True, **resultado})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500