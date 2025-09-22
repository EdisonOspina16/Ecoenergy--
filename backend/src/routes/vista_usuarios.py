import sys
sys.path.append("src")
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from controller.controladorUsuarios import registrar_usuario, verificar_credenciales, actualizar_contraseña, obtener_usuario_por_id
from controller import controladorDispositivos as cd 

blueprint = Blueprint('vista_usuarios', __name__, template_folder="Templates")


# para que no lo deje ver el perfil si el usario no esta iniciado
def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        usuario = session.get('usuario')
        if not usuario:               
            flash("Debes iniciar sesión para acceder a esta página", "warning")
            return redirect(url_for('vista_usuarios.login'))
        return f(*args, **kwargs)
    return decorador


@blueprint.route('/')
def inicio():
    usuario = session.get('usuario')
    productos_por_categoria = cd.obtener_dispositivos_por_categoria()

    if usuario:
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



@blueprint.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        correo = request.form['correo']
        nueva_contraseña = request.form['nueva_contraseña']

        exito = actualizar_contraseña(correo, nueva_contraseña)
        if exito:
            flash("Contraseña actualizada correctamente", "success")
            return redirect(url_for('vista_usuarios.login'))
        else:
            flash("No se encontró el correo", "danger")

    return render_template('recuperar.html')

    
# -----------------------------------------

# perfil
@blueprint.route('/perfil')
@login_requerido
def perfil():
    # Obtener datos básicos de la sesión
    usuario_sesion = session.get('usuario')
    
    if not usuario_sesion:
        flash("Debes iniciar sesión para acceder a esta página", "warning")
        return redirect(url_for('vista_usuarios.login'))
    
    # Obtener todos los datos del usuario desde la base de datos
    usuario_completo = obtener_usuario_por_id(usuario_sesion['id'])
    
    if not usuario_completo:
        flash("Error al cargar los datos del usuario", "danger")
        return redirect(url_for('vista_usuarios.inicio'))
    
    # Crear diccionario con todos los datos
    usuario_data = {
        'id': usuario_completo.id,
        'nombre': usuario_completo.nombre,
        'correo': usuario_completo.correo,
        'es_admin': usuario_completo.es_admin,
        'fecha_registro': usuario_completo.fecha_registro.strftime('%d/%m/%Y %H:%M') if usuario_completo.fecha_registro else 'No disponible',
        'telefono': usuario_completo.telefono,
        'direccion': usuario_completo.direccion,
        'ciudad': usuario_completo.ciudad,
        'estrato': usuario_completo.estrato
    }
    
    return render_template('perfil.html', usuario=usuario_data)

# -----------------------------------------

@blueprint.route('/registro_paso2', methods=['GET', 'POST'])
def registro_paso2():
    datos1 = session.get('registro_step1')
    if not datos1:
        return redirect(url_for('vista_usuarios.registro'))

    if request.method == 'POST':
        # 1) Recuperamos paso 1 desde session
        nombre      = datos1['nombre']
        correo      = datos1['correo']
        contraseña  = datos1['contraseña']

        # 2) Recuperamos paso 2 desde el form
        telefono    = request.form.get('telefono')
        direccion   = request.form.get('direccion')
        ciudad      = request.form.get('ciudad')
        estrato     = request.form.get('estrato')

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
            flash("Usuario registrado con éxito", "success")
            return redirect(url_for('vista_usuarios.login'))
        else:
            flash("Error al registrar usuario", "danger")
            return redirect(url_for('vista_usuarios.registro'))

    # GET - Mostrar paso 2
    return render_template('registro_paso2.html')