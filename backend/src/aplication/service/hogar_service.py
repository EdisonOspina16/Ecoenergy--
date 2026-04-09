from src.domain.errors import ConexionError
from database import obtener_conexion
from model.hogar import Hogar
from repositories.hogar_repository import HogarRepository
from aplication.validators.hogar_validator import validar_crear_hogar


def crear_hogar(id_usuario: int, direccion: str, nombre_hogar: str) -> Hogar | None:
    """
    Crea un nuevo hogar para un usuario:
    1. Valida id_usuario, nombre_hogar y dirección.
    2. Obtiene conexión a la BD.
    3. Delega el INSERT en el repositorio (fila cruda).
    4. Mapea la fila cruda a un objeto Hogar.
    Retorna el objeto Hogar creado o None si no se insertó.
    """
    validar_crear_hogar(id_usuario, direccion, nombre_hogar)

    conn = obtener_conexion()
    if not conn:
        raise ConexionError("No se pudo conectar a la base de datos")

    try:
        repo = HogarRepository(conn)
        fila = repo.crear_hogar(id_usuario, direccion, nombre_hogar)

        if not fila:
            return None

        return Hogar(
            id_hogar=fila['id_hogar'],
            id_usuario=fila['id_usuario'],
            direccion=fila['direccion'],
            nombre_hogar=fila['nombre_hogar']
        )
    finally:
        conn.close()