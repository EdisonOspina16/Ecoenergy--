from src.domain.errors import ConexionError
from werkzeug.security import generate_password_hash
from database import obtener_conexion
from repositories.usuario_repository import UsuarioRepository
from aplication.validators.usuario_validator import validar_usuario, validar_cambio_contrasena


def registrar_usuario(nombre, apellidos, correo, contrasena):

    conn = obtener_conexion()
    if not conn:
        raise ConexionError("No se pudo conectar a la base de datos")

    try:
        validar_usuario(nombre, apellidos, correo, contrasena)

        hash_contrasena = generate_password_hash(contrasena)

        repo = UsuarioRepository(conn)
        repo.crear_usuario(nombre, apellidos, correo, hash_contrasena)
        return True
    finally:
        conn.close()

def cambiar_contrasena(correo, nueva_contrasena) -> bool:
    conn = obtener_conexion()
    if not conn:
        raise ConexionError("No se pudo conectar a la base de datos")

    try:
        validar_cambio_contrasena(correo, nueva_contrasena)

        nueva_hash = generate_password_hash(nueva_contrasena)

        repo = UsuarioRepository(conn)
        return repo.actualizar_contrasena(
            correo.strip().lower(),
            nueva_hash
        )

    finally:
        conn.close()

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



