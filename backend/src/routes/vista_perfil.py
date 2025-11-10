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
    verificar_dispositivo_existe
)

blueprint_perfil = Blueprint('vista_perfil', __name__)


def login_requerido_perfil(f):
    """Decorador para verificar que el usuario esté autenticado"""
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario = session.get('usuario')
        if not usuario:
            return jsonify({"success": False, "error": "Debes iniciar sesión"}), 401
        return f(*args, **kwargs)
    return decorador


# ⭐ IMPORTANTE: Agregar supports_credentials=True a TODOS los @cross_origin()
@blueprint_perfil.route('/perfil', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_requerido_perfil
def obtener_perfil_completo():
    """Obtiene el perfil del hogar y los dispositivos del usuario autenticado"""
    try:
        usuario = session.get('usuario')
        id_usuario = usuario['id']
        
        # Obtener hogar
        hogar = obtener_hogar_por_usuario(id_usuario)
        
        # Obtener dispositivos
        dispositivos = obtener_dispositivos_por_usuario(id_usuario)
        dispositivos_dict = [disp.to_dict() for disp in dispositivos]
        
        return jsonify({
            'success': True,
            'hogar': hogar.to_dict() if hogar else None,
            'dispositivos': dispositivos_dict
        }), 200
            
    except Exception as e:
        print(f"Error en obtener_perfil_completo: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@blueprint_perfil.route('/perfil', methods=['POST'])
@cross_origin(supports_credentials=True)
@login_requerido_perfil
def guardar_perfil_o_dispositivo():
    """Crea/actualiza el perfil del hogar O registra un nuevo dispositivo según los datos recibidos"""
    try:
        usuario = session.get('usuario')
        id_usuario = usuario['id']
        
        data = request.get_json()
        
        # Determinar si es perfil de hogar o dispositivo
        if 'deviceId' in data and 'nickname' in data:
            # Es un registro de dispositivo
            id_dispositivo_iot = data.get('deviceId')
            alias = data.get('nickname')
            
            if not all([id_dispositivo_iot, alias]):
                return jsonify({
                    'success': False,
                    'error': 'ID del dispositivo y alias son requeridos'
                }), 400
            
            # Verificar si el dispositivo ya existe
            if verificar_dispositivo_existe(id_dispositivo_iot):
                return jsonify({
                    'success': False,
                    'error': 'Este dispositivo ya está registrado'
                }), 400
            
            # Obtener el hogar del usuario
            hogar = obtener_hogar_por_usuario(id_usuario)
            
            if not hogar:
                return jsonify({
                    'success': False,
                    'error': 'Debes crear un perfil de hogar primero'
                }), 400
            
            # Registrar el dispositivo
            dispositivo = crear_dispositivo(
                id_hogar=hogar.id_hogar,
                alias=alias,
                id_dispositivo_iot=id_dispositivo_iot
            )
            
            if dispositivo:
                return jsonify({
                    'success': True,
                    'message': 'Dispositivo registrado exitosamente',
                    'dispositivo': dispositivo.to_dict()
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'error': 'Error al registrar el dispositivo'
                }), 500
        
        else:
            # Es una actualización de perfil de hogar
            direccion = data.get('address')
            nombre_hogar = data.get('nombre_hogar')
            
            if not direccion or not nombre_hogar:
                return jsonify({
                    'success': False,
                    'error': 'La dirección y el nombre del hogar son requeridos'
                }), 400
            
            # Verificar si ya existe un hogar
            hogar_previo = obtener_hogar_por_usuario(id_usuario)
            
            # Crear o actualizar el hogar
            hogar = crear_o_actualizar_hogar(
                id_usuario=id_usuario,
                direccion=direccion,
                nombre_hogar=nombre_hogar
            )
            
            if hogar:
                mensaje = 'Perfil actualizado exitosamente' if hogar_previo else 'Perfil creado exitosamente'
                
                return jsonify({
                    'success': True,
                    'message': mensaje,
                    'hogar': hogar.to_dict()
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': 'Error al guardar el perfil'
                }), 500
        
    except Exception as e:
        print(f"Error en guardar_perfil_o_dispositivo: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


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
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


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
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    