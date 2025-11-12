import sys
sys.path.append("src")

from flask import Blueprint, request, jsonify
from repository.indicadores_repository import guardar_indicador, obtener_indicadores_por_usuario
from model.indicadores import Indicadores

blueprint = Blueprint("vista_indicadores", __name__)

@blueprint.route("/api/indicadores/<int:id_usuario>", methods=["GET"])
def get_indicadores(id_usuario):
    indicadores = obtener_indicadores_por_usuario(id_usuario)
    return jsonify(indicadores), 200

@blueprint.route("/api/indicadores", methods=["POST"])
def post_indicador():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON requerido"}), 400

    usuario_id = data.get("usuario_id")
    energia = data.get("energia_ahorrada_kwh")

    if usuario_id is None or energia is None:
        return jsonify({"error": "usuario_id y energia_ahorrada_kwh son requeridos"}), 400

    factor_co2 = 0.233
    co2_por_arbol = 21.0
    precio_kwh = data.get("precio_per_kwh", 0.15)

    reduccion_co2 = round(float(energia) * factor_co2, 3)
    arboles = round(reduccion_co2 / co2_por_arbol, 3)
    ahorro = round(float(energia) * float(precio_kwh), 2)

    indicador = Indicadores(
        usuario_id=usuario_id,
        energia_ahorrada_kwh=energia,
        reduccion_co2_kg=reduccion_co2,
        arboles_salvados=arboles,
        ahorro_economico=ahorro
    )

    new_id = guardar_indicador(indicador)
    if new_id is None:
        return jsonify({"error": "No se pudo guardar el indicador"}), 500

    return jsonify({
        "message": "Indicador guardado exitosamente",
        "id_indicador": new_id
    }), 201
