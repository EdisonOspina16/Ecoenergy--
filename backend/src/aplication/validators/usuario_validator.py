from domain.errors import ValidacionError
from werkzeug.security import check_password_hash, generate_password_hash
from model.usuario import Usuario
from src.database import obtener_conexion
import re


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


def validar_usuario(nombre, apellidos, correo, contrasena):
    if not es_nombre_valido(nombre):
        raise ValidacionError("Nombre inválido")

    if not es_apellido_valido(apellidos):
        raise ValidacionError("Apellidos inválidos")

    if not es_correo_valido(correo):
        raise ValidacionError("Correo inválido")

    if not es_contrasena_valida(contrasena):
        raise ValidacionError("Contraseña inválida")