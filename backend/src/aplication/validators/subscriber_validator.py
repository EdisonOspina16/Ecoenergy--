from src.domain.errors import ValidacionError
from aplication.validators.usuario_validator import es_correo_valido

def validar_suscripcion(email: str) -> None:
    """
    Valida el correo electrónico para suscripción.
    Reutiliza es_correo_valido() de usuario_validator.
    Lanza ValidacionError si el correo no es válido.
    """
    if not email:
        raise ValidacionError("Correo obligatorio")
 
    if not es_correo_valido(email):
        raise ValidacionError("Correo inválido")