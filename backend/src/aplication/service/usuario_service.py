from domain.errors import ConexionError
from werkzeug.security import generate_password_hash
from database import obtener_conexion
from repositories.usuario_repository import UsuarioRepository
from aplication.validators.usuario_validator import validar_usuario


def registrar_usuario(nombre, apellidos, correo, contrasena):

    conn = obtener_conexion()
    if not conn:
        raise ConexionError("No se pudo conectar a la base de datos")

    try:
        validar_usuario(nombre, apellidos, correo, contrasena)

        hash_contrasena = generate_password_hash(contrasena)

        repo = UsuarioRepository(conn)
        repo.crear_usuario(nombre, apellidos, correo, hash_contrasena)

    finally:
        conn.close()

#-------------------------------------
# Gestor de autenticación
#-------------------------------------
# login_usuario()
# cerrar_sesion()
#-------------------------------------
# Gestor de contraseñas
#-------------------------------------
# solicitar_recuperacion_contrasena()
# cambiar_contrasena()
# resetear_contrasena()
#-------------------------------------
# Gestor de perfil de usuario
#-------------------------------------
# obtener_usuario()
# actualizar_usuario()
# eliminar_usuario()



