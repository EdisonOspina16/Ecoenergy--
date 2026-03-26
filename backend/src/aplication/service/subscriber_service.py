from src.domain.errors import ConexionError, CorreoDuplicadoError
from database import obtener_conexion
from controller.controladorEmail import send_welcome_email
from repositories.subscriber_repository import SubscriberRepository
from aplication.validators.subscriber_validator import validar_suscripcion


def subscribe_user(email: str) -> tuple[bool, str]:
    """
    Registra un usuario como suscriptor y envía correo de bienvenida:
    1. Valida que el correo no esté vacío y tenga formato válido.
    2. Obtiene conexión a la BD.
    3. Delega el INSERT en el repositorio.
    4. Envía correo de bienvenida.
    Retorna (True, mensaje) si exitoso o (False, mensaje) si falla.
    """
    validar_suscripcion(email)

    conn = obtener_conexion()
    if not conn:
        raise ConexionError("No se pudo conectar a la base de datos")

    try:
        repo = SubscriberRepository(conn)
        repo.crear_suscriptor(email)
        send_welcome_email(email)
        return True, "Correo registrado y enviado"

    except CorreoDuplicadoError:
        return False, "Correo ya registrado"

    finally:
        conn.close()