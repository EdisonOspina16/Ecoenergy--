import sys
sys.path.append("src")

from flask import Blueprint, request, jsonify, session
from functools import wraps
from flask_cors import cross_origin
from controller.controladorHogar import (
    obtener_hogar_por_usuario,
    crear_o_actualizar_hogar
)
from controller.controladorDispositivos import (
    obtener_dispositivos_por_usuario,
    crear_dispositivo,
    actualizar_alias_dispositivo,
    eliminar_dispositivo,
    verificar_dispositivo_existe,
    actualizar_estado_dispositivo
)
from aplication.validators.perfil_validators import (
    is_device_payload,
    is_profile_payload,
)
from aplication.service.perfil_service import (
    registrar_tomacorriente,
    seleccionar_accion_perfil,
)
from aplication.service.response_builder import error_response
from repositories.perfil_repository import PerfilRepository

blueprint_perfil = Blueprint('vista_perfil', __name__)

def retornar_jsonify_fallido(e):
    return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def login_requerido_perfil(f):
    """Decorador para verificar que el usuario esté autenticado"""
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario = session.get('usuario')
        if not usuario:
            return jsonify({"success": False, "error": "Debes iniciar sesión"}), 401
        return f(*args, **kwargs)
    return decorador

# IMPORTANTE: Hay que agregar supports_credentials=True a TODOS los @cross_origin()
@blueprint_perfil.route('/perfil', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_requerido_perfil
def obtener_perfil_completo_y_listar_tomacorrientes():
    """Obtiene el perfil del hogar y los dispositivos del usuario autenticado"""
    try:
        usuario = session.get('usuario')
        id_usuario = usuario['id']

        # Obtenenemos hogar
        hogar = obtener_hogar_por_usuario(id_usuario)

        # Obtenenemos dispositivos
        dispositivos = obtener_dispositivos_por_usuario(id_usuario)
        dispositivos_dict = [disp.to_dict() for disp in dispositivos]

        return jsonify({
            'success': True,
            'hogar': hogar.to_dict() if hogar else None,
            'dispositivos': dispositivos_dict
        }), 200

    except Exception as e:
        print(f"Error en obtener perfil completo: {e}")
        retornar_jsonify_fallido(e)

@blueprint_perfil.route('/perfil', methods=['POST'])
@cross_origin(supports_credentials=True)
@login_requerido_perfil
def registrar_tomacorriente_o_guardar_perfil_de_hogar():
    """Registra un nuevo tomacorriente/dispositivo O crea/actualiza el perfil del hogar según los datos recibidos"""
    usuario = session.get('usuario')
    id_usuario = usuario['id']

    data = request.get_json() or {}
    repo = PerfilRepository(
        obtener_hogar=obtener_hogar_por_usuario,
        crear_o_actualizar_hogar=crear_o_actualizar_hogar,
        verificar_dispositivo_existe=verificar_dispositivo_existe,
        crear_dispositivo=crear_dispositivo,
    )

    if is_device_payload(data):
        return registrar_tomacorriente(data, id_usuario, repo)

    if is_profile_payload(data):
        return seleccionar_accion_perfil(data, id_usuario, repo)

    return error_response(
        "La solicitud no coincide con un registro de dispositivo ni perfil",
        400,
    )

@blueprint_perfil.route('/perfil/dispositivo/<int:id_dispositivo>', methods=['PUT'])
@cross_origin(supports_credentials=True)
@login_requerido_perfil
def actualizar_dispositivo(id_dispositivo):
    """Actualiza el alias de un dispositivo"""
    try:
        usuario = session.get('usuario')
        id_usuario = usuario['id']

        data = request.get_json()
        nuevo_alias = data.get('name')

        if not nuevo_alias:
            return jsonify({
                'success': False,
                'error': 'El alias es requerido'
            }), 400

        exito = actualizar_alias_dispositivo(id_dispositivo, id_usuario, nuevo_alias)

        if exito:
            return jsonify({
                'success': True,
                'message': 'Dispositivo actualizado exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Dispositivo no encontrado o no autorizado'
            }), 404

    except Exception as e:
        print(f"Error en actualizar_dispositivo: {e}")
        retornar_jsonify_fallido(e)


@blueprint_perfil.route('/perfil/dispositivo/<int:id_dispositivo>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
@login_requerido_perfil
def eliminar_dispositivo_route(id_dispositivo):
    """Elimina un dispositivo del hogar"""
    try:
        usuario = session.get('usuario')
        id_usuario = usuario['id']

        exito = eliminar_dispositivo(id_dispositivo, id_usuario)

        if exito:
            return jsonify({
                'success': True,
                'message': 'Dispositivo eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Dispositivo no encontrado o no autorizado'
            }), 404

    except Exception as e:
        print(f"Error en eliminar_dispositivo: {e}")
        return retornar_jsonify_fallido(e)

@blueprint_perfil.route('/perfil/dispositivo/<int:id_dispositivo>/estado', methods=['PUT'])
@cross_origin(supports_credentials=True)
@login_requerido_perfil
def cambiar_estado_dispositivo(id_dispositivo):
    """Cambia el estado activo/inactivo del dispositivo (encendido/apagado)."""
    try:
        usuario = session.get('usuario')
        id_usuario = usuario['id']

        data = request.get_json()
        nuevo_estado = data.get('estado_activo')  # True o False desde el front

        if nuevo_estado is None:
            return jsonify({
                'success': False,
                'error': 'El estado del dispositivo es requerido (True/False)'
            }), 400

        exito = actualizar_estado_dispositivo(id_dispositivo, id_usuario, nuevo_estado)

        if exito:
            return jsonify({
                'success': True,
                'message': f'Dispositivo {"encendido" if nuevo_estado else "apagado"} correctamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Dispositivo no encontrado o no autorizado'
            }), 404

    except Exception as e:
        print(f"Error en cambiar_estado_dispositivo: {e}")
        retornar_jsonify_fallido(e)
