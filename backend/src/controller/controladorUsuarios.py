import sys
sys.path.append("src")

from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
from model.usuario import Usuario
from src.database import obtener_conexion
import re


def verificar_credenciales(correo, contrasena_input):
    """
    Verifica si el correo y la contrasena (comparada con hash) coinciden.
    Retorna objeto Usuario con todos los campos.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = cur.fetchone()

        cur.close()
        conn.close()

        if usuario and check_password_hash(usuario['contrasena'], contrasena_input):
            return Usuario(
                id_usuario=usuario['id_usuario'],
                nombre=usuario['nombre'],
                apellidos=usuario['apellidos'],
                correo=usuario['correo'],
                contrasena=usuario['contrasena']
            )
        return None
    except Exception as e:
        print(f"Error en login: {e}")
        return None


def actualizar_contrasena(correo, nueva_contrasena):
    """
    Actualiza la contrasena de un usuario con hashing.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        nueva_hash = generate_password_hash(nueva_contrasena)

        cur.execute("""
            UPDATE usuarios
            SET contrasena = %s
            WHERE correo = %s
        """, (nueva_hash, correo))

        conn.commit()
        cur.close()
        conn.close()

        return cur.rowcount > 0
    except Exception as e:
        print(f"Error al actualizar contrasena: {e}")
        return False


#para mostrar los datos del usuario
def obtener_usuario_por_id(id_usuario):
    try:
        conn = obtener_conexion()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
        fila = cur.fetchone()

        cur.close()
        conn.close()

        if fila:
            return Usuario(
                id_usuario=fila['id_usuario'],
                nombre=fila['nombre'],
                apellidos=fila['apellidos'],
                correo=fila['correo'],
                contrasena=fila['contrasena'],
                fecha_registro=fila['fecha_registro'],
            )
    except Exception as e:
        print(f"Error al obtener usuario por ID: {e}")
    return None


