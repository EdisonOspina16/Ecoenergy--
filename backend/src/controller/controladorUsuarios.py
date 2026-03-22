import sys
sys.path.append("src")

from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
from model.usuario import Usuario
from src.database import obtener_conexion
import re


# -----------------------------------------
# CRUD USUARIOS
# -----------------------------------------

def crear_usuario(nombre, correo, contrasena):
    """
    Crea un nuevo usuario con la contrasena hasheada.
    """
    conn = obtener_conexion()
    if conn:
        try:
            hash_contrasena = generate_password_hash(contrasena)
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO usuarios (nombre, correo, contrasena) VALUES (%s, %s, %s)",
                    (nombre, correo, hash_contrasena)
                )
                conn.commit()
                return True
        except Exception as e:
            print("Error al crear usuario:", e)
        finally:
            conn.close()
    return False

def obtener_usuario_por_correo(correo):
    conn = obtener_conexion()
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
                usuario = cur.fetchone()
                if usuario:
                    return {
                        'id_usuario': usuario['id_usuario'],
                        'nombre': usuario['nombre'],
                        'correo': usuario['correo'],
                        'contrasena': usuario['contrasena'],
                        'fecha_registro': usuario['fecha_registro']
                    }
                return None
        except Exception as e:
            print("Error al obtener usuario:", e)
        finally:
            conn.close()
    return None

def actualizar_usuario(correo, nuevo_nombre, nueva_contrasena):
    """
    Actualiza nombre y contrasena (la contrasena será hasheada).
    """
    conn = obtener_conexion()
    if conn:
        try:
            hash_contrasena = generate_password_hash(nueva_contrasena)
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE usuarios SET nombre = %s, contrasena = %s WHERE correo = %s",
                    (nuevo_nombre, hash_contrasena, correo)
                )
                conn.commit()
                return True
        except Exception as e:
            print("Error al actualizar usuario:", e)
        finally:
            conn.close()
    return False


def eliminar_usuario(correo):
    conn = obtener_conexion()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM usuarios WHERE correo = %s", (correo,))
                conn.commit()
                return True
        except Exception as e:
            print("Error al eliminar usuario:", e)
        finally:
            conn.close()
    return False

# -----------------------------------------
# FUNCIONES DEL REGISTRO, LOGIN, RECUPERAR
# -----------------------------------------


def obtener_usuarios():
    """
    Retorna una lista de objetos Usuario con todos los campos.
    """
    usuarios = []
    try:
        conn = obtener_conexion()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM usuarios")
        filas = cur.fetchall()

        for fila in filas:
            usuario = Usuario(
                id_usuario=fila['id_usuario'],
                nombre=fila['nombre'],
                apellidos=fila['apellidos'],
                correo=fila['correo'],
                contrasena=fila['contrasena'],
                fecha_registro=fila['fecha_registro']
            )
            usuarios.append(usuario)

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
    return usuarios

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

# vamos a ver?
def actualizar_datos_adicionales(correo, telefono, direccion, ciudad, estrato):
    """
    Actualiza los datos adicionales del usuario.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor()

        cur.execute("""
            UPDATE usuarios
            SET telefono = %s,
                direccion = %s,
                ciudad = %s,
                estrato = %s
            WHERE correo = %s
        """, (telefono, direccion, ciudad, estrato, correo))

        conn.commit()
        cur.close()
        conn.close()

        return cur.rowcount > 0
    except Exception as e:
        print(f"Error al actualizar datos adicionales: {e}")
        return False
