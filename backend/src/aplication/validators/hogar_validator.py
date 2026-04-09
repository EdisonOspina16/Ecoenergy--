from src.domain.errors import ValidacionError
from aplication.validators.usuario_validator import es_id_usuario_valido
import re


def es_nombre_hogar_valido(nombre_hogar: str) -> bool:
    """
    Valida el nombre del hogar:
    - No nulo ni vacío
    - Entre 2 y 50 caracteres
    - Solo letras, números, espacios y guion
    - Sin caracteres especiales como *, #, @, etc.
    """
    if not isinstance(nombre_hogar, str):
        return False
    nombre_hogar = nombre_hogar.strip()
    if len(nombre_hogar) < 2 or len(nombre_hogar) > 50:
        return False
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s\-]+$"
    return re.match(patron, nombre_hogar) is not None


def es_direccion_valida(direccion: str) -> bool:
    """
    Valida la dirección del hogar:
    - No nula ni vacía
    - Entre 5 y 100 caracteres
    - Permite letras, números, espacios, guion, #, coma y punto
    """
    if not isinstance(direccion, str):
        return False
    direccion = direccion.strip()
    if len(direccion) < 5 or len(direccion) > 100:
        return False
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s\-#,\.]+$"
    return re.match(patron, direccion) is not None


def validar_crear_hogar(id_usuario, direccion: str, nombre_hogar: str) -> None:
    """
    Valida los datos necesarios para crear un hogar:
    - id_usuario válido (entero positivo)
    - nombre_hogar con formato válido
    - dirección con formato válido
    Lanza ValidacionError si alguno falla.
    """
    if not es_id_usuario_valido(id_usuario):
        raise ValidacionError("ID de usuario inválido")

    if not es_nombre_hogar_valido(nombre_hogar):
        raise ValidacionError("Nombre del hogar inválido")

    if not es_direccion_valida(direccion):
        raise ValidacionError("Dirección inválida")