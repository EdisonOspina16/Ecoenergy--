class UsuarioError(Exception):
    pass

class ValidacionError(UsuarioError):
    pass

class ConexionError(UsuarioError):
    pass

class PersistenciaError(UsuarioError):
    pass

class CorreoDuplicadoError(PersistenciaError):
    pass


# Generales para perfil/dispositivos
class ValidationError(Exception):
    """Error de validación de entrada."""


class ConflictError(Exception):
    """Error por datos en conflicto, como duplicados."""


class NotFoundError(Exception):
    """Error cuando un recurso no existe."""
