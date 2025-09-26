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
<<<<<<< HEAD
        return render_template('inicio.html', products_by_category=productos_por_categoria, devices=[], usuario=usuario)
    else:
        return render_template('inicio.html', products_by_category=productos_por_categoria, devices=[],usuario=usuario )


# Para cerrar sesión
@blueprint.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for('vista_usuarios.inicio'))


# Ruta para mostrar el formulario de registro
@blueprint.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Guardamos en session lo necesario del paso 1
        session['registro_step1'] = {
            'nombre':     request.form['nombre'],
            'correo':     request.form['correo'],
            'contraseña': request.form['contraseña']
        }
        return redirect(url_for('vista_usuarios.registro_paso2'))

    # GET Mostrar el primer formulario
    return render_template('registro.html')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        usuario = verificar_credenciales(correo, contraseña)

        if usuario:
            session['usuario'] = usuario.to_dict()

            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('vista_usuarios.inicio'))
        
        else:
            flash("Credenciales inválidas", "danger")

    return render_template('login.html')    
=======
        session['usuario'] = usuario.to_dict()

        return jsonify({
            "message": "Inicio de sesión exitoso", 
            "redirect": "/dashboard",
            "usuario": usuario.to_dict()
        })
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401    
>>>>>>> backend



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
