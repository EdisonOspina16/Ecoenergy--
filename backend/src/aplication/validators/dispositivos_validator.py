from aplication.validators.usuario_validator import es_id_usuario_valido
from src.domain.errors import ValidacionError

def validar_listar_dispositivos(id_usuario) -> None:
    if not es_id_usuario_valido(id_usuario):
        raise ValidacionError("ID de usuario inválido")
    
