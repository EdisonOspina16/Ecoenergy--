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

# ---- Validaciones de datos de registro ----

def es_nombre_valido(nombre: str) -> bool:
    """
    Valida el nombre:
    - No nulo ni vacío
    - Entre 2 y 50 caracteres
    - Solo letras (incluye tildes) y espacios.
    """
    if not isinstance(nombre, str):
        return False
    nombre = nombre.strip()
    if len(nombre) < 2 or len(nombre) > 50:
        return False
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$"
    return re.match(patron, nombre) is not None


def es_apellido_valido(apellidos: str) -> bool:
    """
    Valida el apellido:
    - No nulo ni vacío
    - Mínimo 2 caracteres
    - Letras (incluye tildes), espacios y guion.
    """
    if not isinstance(apellidos, str):
        return False
    apellidos = apellidos.strip()
    if len(apellidos) < 2:
        return False
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\-]+$"
    return re.match(patron, apellidos) is not None


def es_correo_valido(correo: str) -> bool:
    """
    Valida el correo:
    - No nulo ni vacío
    - Sin espacios
    - Longitud máxima 254 caracteres
    - Formato básico RFC (local@dominio.tld)
    """
    if not isinstance(correo, str):
        return False
    correo = correo.strip()
    if not correo:
        return False
    if " " in correo:
        return False
    if len(correo) > 254:
        return False
    patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(patron, correo) is not None


def es_contrasena_valida(contrasena: str) -> bool:
    """
    Valida la contrasena:
    - String no vacío
    - Entre 8 y 128 caracteres
    - Sin espacios
    - Sin caracteres no ASCII (evita emojis)
    - Debe contener al menos: una mayúscula, una minúscula,
      un dígito y un carácter especial.
    """
    if not isinstance(contrasena, str):
        return False
    if contrasena == "":
        return False
    if len(contrasena) < 8 or len(contrasena) > 128:
        return False
    if any(ch.isspace() for ch in contrasena):
        return False
    if any(ord(ch) > 126 for ch in contrasena):
        return False

    tiene_mayus = any(c.isupper() for c in contrasena)
    tiene_minus = any(c.islower() for c in contrasena)
    tiene_digito = any(c.isdigit() for c in contrasena)
    tiene_especial = any(not c.isalnum() and not c.isspace() for c in contrasena)

    return tiene_mayus and tiene_minus and tiene_digito and tiene_especial


def registrar_usuario(nombre, apellidos, correo, contrasena):
    """
    Registra un usuario nuevo con contrasena hasheada y datos adicionales.
    """
    try:
        conn = obtener_conexion()
        if not conn:
            print("No se pudo conectar a la base de datos")
            return False
            
        print("Conexión a la base de datos establecida")
        cur = conn.cursor()

        hash_contrasena = generate_password_hash(contrasena)
        print("contrasena hasheada correctamente")

        cur.execute("""
            INSERT INTO usuarios (nombre, apellidos, correo, contrasena)
            VALUES (%s, %s, %s, %s)
        """, (nombre, apellidos, correo, hash_contrasena))

        conn.commit()
        print("Usuario insertado en la base de datos")
        
        cur.close()
        conn.close()
        print("Conexión cerrada correctamente")
        return True
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        print(f"Tipo de error: {type(e).__name__}")
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
    