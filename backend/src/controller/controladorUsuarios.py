import sys
sys.path.append("src")

import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
from model.usuario import Usuario
from SecretConfig import PGHOST, PGDATABASE, PGUSER, PGPASSWORD


def obtener_conexion():
    """
    Conexión a la base de datos.
    """
    try:
        return psycopg2.connect(
            host=PGHOST,
            database=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD
        )
    except Exception as e:
        print("Error de conexión:", e)
        return None

# -----------------------------------------
# CRUD USUARIOS
# -----------------------------------------

def crear_usuario(nombre, correo, contraseña):
    """
    Crea un nuevo usuario con la contraseña hasheada.
    """
    conn = obtener_conexion()
    if conn:
        try:
            hash_contraseña = generate_password_hash(contraseña)
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO usuarios (nombre, correo, contraseña) VALUES (%s, %s, %s)",
                    (nombre, correo, hash_contraseña)
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
                        'id': usuario['id'],
                        'nombre': usuario['nombre'],
                        'correo': usuario['correo'],
                        'contraseña': usuario['contraseña'],
                        'fecha_registro': usuario['fecha_registro'],
                        'es_admin': usuario['es_admin'],
                        'telefono': usuario.get('telefono'),
                        'direccion': usuario.get('direccion'),
                        'ciudad': usuario.get('ciudad'),
                        'estrato': usuario.get('estrato')
                    }
                return None
        except Exception as e:
            print("Error al obtener usuario:", e)
        finally:
            conn.close()
    return None

def actualizar_usuario(correo, nuevo_nombre, nueva_contraseña):
    """
    Actualiza nombre y contraseña (la contraseña será hasheada).
    """
    conn = obtener_conexion()
    if conn:
        try:
            hash_contraseña = generate_password_hash(nueva_contraseña)
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE usuarios SET nombre = %s, contraseña = %s WHERE correo = %s",
                    (nuevo_nombre, hash_contraseña, correo)
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

def registrar_usuario(nombre, correo, contraseña, telefono=None, direccion=None, ciudad=None, estrato=None):
    """
    Registra un usuario nuevo con contraseña hasheada y datos adicionales.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor()

        hash_contraseña = generate_password_hash(contraseña)

        cur.execute("""
            INSERT INTO usuarios (nombre, correo, contraseña, telefono, direccion, ciudad, estrato)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, correo, hash_contraseña, telefono, direccion, ciudad, estrato))

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False


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
                id=fila['id'],
                nombre=fila['nombre'],
                correo=fila['correo'],
                contraseña=fila['contraseña'],
                fecha_registro=fila['fecha_registro'],
                es_admin=fila.get('es_admin', False),
                telefono=fila.get('telefono'),
                direccion=fila.get('direccion'),
                ciudad=fila.get('ciudad'),
                estrato=fila.get('estrato')
            )
            usuarios.append(usuario)

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
    return usuarios

def verificar_credenciales(correo, contraseña_input):
    """
    Verifica si el correo y la contraseña (comparada con hash) coinciden.
    Retorna objeto Usuario con todos los campos.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = cur.fetchone()

        cur.close()
        conn.close()

        if usuario and check_password_hash(usuario['contraseña'], contraseña_input):
            return Usuario(
                id=usuario['id'],
                nombre=usuario['nombre'],
                correo=usuario['correo'],
                contraseña=usuario['contraseña'],
                es_admin=usuario['es_admin'],
                fecha_registro=usuario.get('fecha_registro'),
                telefono=usuario.get('telefono'),
                direccion=usuario.get('direccion'),
                ciudad=usuario.get('ciudad'),
                estrato=usuario.get('estrato')
            )
        return None
    except Exception as e:
        print(f"Error en login: {e}")
        return None

def actualizar_contraseña(correo, nueva_contraseña):
    """
    Actualiza la contraseña de un usuario con hashing.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        nueva_hash = generate_password_hash(nueva_contraseña)

        cur.execute("""
            UPDATE usuarios
            SET contraseña = %s
            WHERE correo = %s
        """, (nueva_hash, correo))

        conn.commit()
        cur.close()
        conn.close()

        return cur.rowcount > 0
    except Exception as e:
        print(f"Error al actualizar contraseña: {e}")
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
                id=fila['id'],
                nombre=fila['nombre'],
                correo=fila['correo'],
                contraseña=fila['contraseña'],
                fecha_registro=fila['fecha_registro'],
                es_admin=fila.get('es_admin', False),
                telefono=fila.get('telefono'),
                direccion=fila.get('direccion'),
                ciudad=fila.get('ciudad'),
                estrato=fila.get('estrato')
            )
    except Exception as e:
        print(f"Error al obtener usuario por ID: {e}")
    return None

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