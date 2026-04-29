from test.screenplay.actions.request import SendRequest


class IniciarSesion:
    def __init__(self, correo: str, contrasena: str):
        self.correo = correo
        self.contrasena = contrasena

    def perform_as(self, actor):
        actor.attempts_to(
            SendRequest("post", "/login", {"correo": self.correo, "contrasena": self.contrasena})
        )
