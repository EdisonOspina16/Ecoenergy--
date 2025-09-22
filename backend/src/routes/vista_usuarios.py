import sys
sys.path.append("src")
from functools import wraps

from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from controller.controladorUsuarios import registrar_usuario, verificar_credenciales, actualizar_contraseña, obtener_usuario_por_id
from controller import controladorDispositivos as cd 

blueprint = Blueprint('vista_usuarios', __name__)


# para que no lo deje ver el perfil si el usario no esta iniciado
def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario = session.get('usuario')
        if not usuario:               
            return jsonify({"error": "Debes iniciar sesión para acceder a esta página"}), 401
        if usuario.get('es_admin'):
            return jsonify({"redirect": "/admin"})
        return f(*args, **kwargs)
    return decorador


@blueprint.route('/')
def inicio():
    return {"message": "Hola Mundo, bienvenido a EcoEnergy"}

# Para cerrar sesión
@blueprint.route('/logout', methods=['POST'])
@cross_origin()
def logout():
    session.clear()
    return jsonify({"message": "Sesión cerrada exitosamente", "redirect": "/login"})


# Ruta para el registro paso 1
@blueprint.route('/registro/paso1', methods=['POST'])
@cross_origin()
def registro_paso1():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['nombre', 'correo', 'contraseña']):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    
    # Guardamos en session lo necesario del paso 1
    session['registro_step1'] = {
        'nombre':     data['nombre'],
        'correo':     data['correo'],
        'contraseña': data['contraseña']
    }
    
    return jsonify({"message": "Paso 1 completado", "redirect": "/registro/paso2"})


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

        if usuario.es_admin:
            return jsonify({
                "message": "Inicio de sesión exitoso", 
                "redirect": "/admin",
                "usuario": usuario.to_dict()
            })
        else:
            return jsonify({
                "message": "Inicio de sesión exitoso", 
                "redirect": "/dashboard",
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

    
# -----------------------------------------

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

# -----------------------------------------

@blueprint.route('/registro/paso2', methods=['POST'])
@cross_origin()
def registro_paso2():
    datos1 = session.get('registro_step1')
    if not datos1:
        return jsonify({"error": "Debes completar el paso 1 primero", "redirect": "/registro"}), 400

    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Faltan datos del paso 2"}), 400

    # 1) Recuperamos paso 1 desde session
    nombre      = datos1['nombre']
    correo      = datos1['correo']
    contraseña  = datos1['contraseña']

    # 2) Recuperamos paso 2 desde el JSON
    telefono    = data.get('telefono')
    direccion   = data.get('direccion')
    ciudad      = data.get('ciudad')
    estrato     = data.get('estrato')

    # Guardamos en la BD
    exito = registrar_usuario(
        nombre=nombre,
        correo=correo,
        contraseña=contraseña,
        telefono=telefono,
        direccion=direccion,
        ciudad=ciudad,
        estrato=estrato
    )

    # Limpiamos session de los datos temporales
    session.pop('registro_step1', None)

    if exito:
        return jsonify({
            "message": "Usuario registrado con éxito", 
            "redirect": "/login"
        })
    else:
        return jsonify({"error": "Error al registrar usuario"}), 500