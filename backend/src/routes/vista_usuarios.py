import sys
sys.path.append("src")
from functools import wraps

from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from controller.controladorUsuarios import registrar_usuario, verificar_credenciales, actualizar_contraseña, obtener_usuario_por_id


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
    return {"message": "Hola Mundo, bienvenido a EcoEnergy"}

# Ruta para el registro
@blueprint.route('/registro', methods=['POST'])
@cross_origin()
def registro():
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

