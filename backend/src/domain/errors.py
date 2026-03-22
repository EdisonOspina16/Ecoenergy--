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
