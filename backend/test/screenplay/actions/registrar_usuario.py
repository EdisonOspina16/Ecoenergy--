from test.screenplay.actions.request import SendRequest


class RegistrarUsuario:
    """
    Tarea Screenplay: registrar un nuevo usuario enviando
    nombre, apellidos, correo y contrasena al endpoint /registro.
    """

    def __init__(self, nombre: str, apellidos: str, correo: str, contrasena: str):
        self.nombre = nombre
        self.apellidos = apellidos
        self.correo = correo
        self.contrasena = contrasena

    def perform_as(self, actor):
        actor.attempts_to(
            SendRequest(
                "post",
                "/registro",
                {
                    "nombre": self.nombre,
                    "apellidos": self.apellidos,
                    "correo": self.correo,
                    "contrasena": self.contrasena,
                },
            )
        )


class RegistrarUsuarioSinCampos:
    """
    Tarea Screenplay: intentar registrar un usuario sin los campos requeridos
    para verificar la validación de la API.
    """

    def perform_as(self, actor):
        actor.attempts_to(
            SendRequest("post", "/registro", {})
        )
