from src.domain.errors import ConexionError
from database import obtener_conexion
from model.dispositivo import Dispositivo
from repositories.dispositivos_repository import DispositivoRepository
from aplication.validators.dispositivos_validator import validar_listar_dispositivos


def listar_dispositivos(id_usuario: int) -> list:
    """
    Lista todos los dispositivos asociados al hogar de un usuario:
    1. Valida que el id_usuario sea válido.
    2. Obtiene conexión a la BD.
    3. Delega la consulta en el repositorio (filas crudas).
    4. Mapea las filas crudas a objetos Dispositivo.
    Retorna lista de Dispositivo o lista vacía si no tiene ninguno.
    """
    validar_listar_dispositivos(id_usuario)

    conn = obtener_conexion()
    if not conn:
        raise ConexionError("No se pudo conectar a la base de datos")

    try:
        repo = DispositivoRepository(conn)
        filas = repo.obtener_por_usuario(id_usuario)

        return [
            Dispositivo(
                id_dispositivos=fila['id_dispositivos'],
                id_hogar=fila['id_hogar'],
                alias=fila['alias'],
                id_dispositivo_iot=fila['id_dispositivo_iot'],
                tipo_dispositivo_ia=fila['tipo_dispositivo_ia'],
                estado_activo=fila['estado_activo'],
                fecha_conexion=fila['fecha_conexion']
            )
            for fila in filas
        ]
    finally:
        conn.close()

def obtener_dispositivos() -> list:
    """
    Obtiene todos los dispositivos con su estado y último consumo registrado:
    1. Obtiene conexión a la BD.
    2. Delega la consulta en el repositorio (filas crudas).
    3. Mapea las filas crudas a dicts con nombre, consumo, estado y watts.
    Retorna lista de dicts o lista vacía si no hay dispositivos.
    No requiere validación porque no recibe parámetros de entrada.
    """
    conn = obtener_conexion()
    if not conn:
        raise ConexionError("No se pudo conectar a la base de datos")
 
    try:
        repo = DispositivoRepository(conn)
        filas = repo.obtener_dispositivos_con_consumo()
 
        return [
            {
                "nombre": fila[0] or fila[3] or "Dispositivo Sin Nombre",
                "consumo": float(fila[1]) / 1000 if fila[1] else 0.0,
                "estado": "Encendido" if fila[2] else "Apagado",
                "watts": float(fila[1]) if fila[1] else 0.0,
            }
            for fila in filas
        ]
    finally:
        conn.close()