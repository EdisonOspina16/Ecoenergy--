import sys
sys.path.append("src")
from functools import wraps

from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from controller.controladorUsuarios import registrar_usuario, verificar_credenciales, actualizar_contraseña, obtener_usuario_por_id
from flasgger import Swagger

blueprint = Blueprint('vista_usuarios', __name__)



# para que no lo deje ver el perfil si el usario no esta iniciado
def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario = session.get('usuario')
        if not usuario:               
            return jsonify({"error": "Debes iniciar sesión para acceder a esta página"}), 401
        return f(*args, **kwargs)
    return decorador


@blueprint.route('/')
def inicio():
    """
    Mensaje de bienvenida
    ---
    tags:
      - General
    responses:
     200:
      description: Mensaje de bienvenida
    """
    return {"message": "Hola Mundo, bienvenido a EcoEnergy"}

# Ruta para el registro
@blueprint.route('/registro', methods=['POST'])
@cross_origin()
def registro():
    """
    Registro de usuario
    ---
    tags:
      - Usuarios
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              nombre:
                type: string
                example: Juan
              apellidos:
                type: string
                example: Pérez
              correo:
                type: string
                example: juan@mail.com
              contraseña:
                type: string
                example: 123456
    responses:
      200:
        description: Usuario registrado con éxito
      400:
        description: Faltan campos requeridos
      500:
        description: Error al registrar usuario
    """
    data = request.get_json()
    
    if not data or not all(key in data for key in ['nombre', 'apellidos', 'correo', 'contraseña']):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    
    # Obtener datos del formulario
    nombre      = data['nombre']
    apellidos   = data['apellidos']
    correo      = data['correo']
    contraseña  = data['contraseña']
    
    print(f"Registro: {nombre}, {apellidos}, {correo}")

    # Guardamos en la BD
    exito = registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contraseña=contraseña
    )

    if exito:
        return jsonify({
            "message": "Usuario registrado con éxito", 
            "redirect": "/login"
        })
    else:
        return jsonify({"error": "Error al registrar usuario"}), 500


@blueprint.route('/login', methods=['POST'])
@cross_origin()
def login():
    """
    Inicio de sesión
    ---
    tags:
      - Usuarios
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              correo:
                type: string
                example: juan@mail.com
              contraseña:
                type: string
                example: 123456
    responses:
      200:
        description: Inicio de sesión exitoso
      400:
        description: Faltan campos requeridos
      401:
        description: Credenciales inválidas
    """
    data = request.get_json()
    
    if not data or not all(key in data for key in ['correo', 'contraseña']):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    
    correo = data['correo']
    contraseña = data['contraseña']

    usuario = verificar_credenciales(correo, contraseña)

    if usuario:
        session['usuario'] = usuario.to_dict()

        return jsonify({
            "message": "Inicio de sesión exitoso", 
            "redirect": "/home",
            "usuario": usuario.to_dict()
        })
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401    



@blueprint.route('/recuperar', methods=['POST'])
@cross_origin()
def recuperar():
    """
    Recuperar contraseña
    ---
    tags:
      - Usuarios
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              correo:
                type: string
                example: juan@mail.com
              nueva_contraseña:
                type: string
                example: 654321
    responses:
      200:
        description: Contraseña actualizada correctamente
      400:
        description: Faltan campos requeridos
      404:
        description: No se encontró el correo
    """
    data = request.get_json()
    
    if not data or not all(key in data for key in ['correo', 'nueva_contraseña']):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    
    correo = data['correo']
    nueva_contraseña = data['nueva_contraseña']

    exito = actualizar_contraseña(correo, nueva_contraseña)
    if exito:
        return jsonify({
            "message": "Contraseña actualizada correctamente", 
            "redirect": "/login"
        })
    else:
        return jsonify({"error": "No se encontró el correo"}), 404

    
# -----------------------------------------
"""
# perfil
@blueprint.route('/perfil', methods=['GET'])
@cross_origin()
@login_requerido
def perfil():
    # Obtener datos básicos de la sesión
    usuario_sesion = session.get('usuario')
    
    if not usuario_sesion:
        return jsonify({"error": "Debes iniciar sesión para acceder a esta página"}), 401
    
    # Obtener todos los datos del usuario desde la base de datos
    usuario_completo = obtener_usuario_por_id(usuario_sesion['id'])
    
    if not usuario_completo:
        return jsonify({"error": "Error al cargar los datos del usuario"}), 500
    
    # Crear diccionario con todos los datos
    usuario_data = {
        'id': usuario_completo.id,
        'nombre': usuario_completo.nombre,
        'correo': usuario_completo.correo,
        'fecha_registro': usuario_completo.fecha_registro.strftime('%d/%m/%Y %H:%M') if usuario_completo.fecha_registro else 'No disponible',
    }
    
    return jsonify({"usuario": usuario_data})
"""
# -----------------------------------------
