import sys
sys.path.append("src")
from functools import wraps

from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from controller.controladorUsuarios import verificar_credenciales
from aplication.service.usuario_service import registrar_usuario, cambiar_contrasena
from src.domain.errors import ConexionError, ValidacionError


blueprint_Usuarios = Blueprint('vista_usuarios', __name__)
ERROR_CAMPOS_REQUERIDOS = {"error": "Faltan campos requeridos"}


# para que no lo deje ver el perfil si el usario no esta iniciado
def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario = session.get('usuario')
        if not usuario:
            print("No hay sesión activa - Redirigiendo a login")
            return jsonify({"error": "Debes iniciar sesión para acceder a esta página"}), 401
        print(f"Sesión activa para usuario: {usuario.get('correo')}")
        return f(*args, **kwargs)
    return decorador


# Ruta para el registro
@blueprint_Usuarios.route('/registro', methods=['POST'])
@cross_origin(supports_credentials=True)
def registro():
    data = request.get_json()

    if not data or not all(key in data for key in ['nombre', 'apellidos', 'correo', 'contrasena']):
        return jsonify(ERROR_CAMPOS_REQUERIDOS), 400

    # Obtener datos del formulario
    nombre      = data['nombre']
    apellidos   = data['apellidos']
    correo      = data['correo']
    contrasena  = data['contrasena']

    print(f"Registro: {nombre}, {apellidos}, {correo}")

    # Guardamos en la BD
    exito = registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena
    )

    if exito:
        return jsonify({
            "message": "Usuario registrado con éxito",
            "redirect": "/login"
        })
    else:
        return jsonify({"error": "Error al registrar usuario"}), 500


@blueprint_Usuarios.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json()

    if not data or not all(key in data for key in ['correo', 'contrasena']):
        return jsonify(ERROR_CAMPOS_REQUERIDOS), 400

    correo = data['correo']
    contrasena = data['contrasena']

    usuario = verificar_credenciales(correo, contrasena)

    if usuario:
        #  CRÍTICO: Hacer la sesión permanente
        session.permanent = True
        session['usuario'] = usuario.to_dict()

        print(f"Login exitoso para: {correo}")
        print(f"Sesión guardada: {session.get('usuario')}")

        return jsonify({
            "success": True,
            "message": "Inicio de sesión exitoso",
            "redirect": "/home",
            "usuario": usuario.to_dict()
        })
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401


@blueprint_Usuarios.route('/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
    """Cierra la sesión del usuario"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Sesión cerrada exitosamente'
    }), 200

@blueprint_Usuarios.route('/recuperar', methods=['POST'])
@cross_origin(supports_credentials=True)
def recuperar():
    data = request.get_json()

    if not data or not all(key in data for key in ['correo', 'nueva_contrasena']):
        return jsonify(ERROR_CAMPOS_REQUERIDOS), 400

    correo = data['correo']
    nueva_contrasena = data['nueva_contrasena']

    try:
        # Usa el nombre correcto según tu proyecto
        exito = cambiar_contrasena(correo, nueva_contrasena)

        if exito:
            return jsonify({
                "message": "contrasena actualizada correctamente",
                "redirect": "/login"
            }), 200
        else:
            return jsonify({"error": "No se encontró el correo"}), 404

    except ValidacionError as e:
        return jsonify({"error": str(e)}), 400

    except ConexionError as e:
        return jsonify({"error": str(e)}), 500
