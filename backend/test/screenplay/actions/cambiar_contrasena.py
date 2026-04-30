from test.screenplay.actions.request import SendRequest

class CambiarContrasena(SendRequest):
    def __init__(self, correo: str, nueva_contrasena: str):
        super().__init__(
            method="post",
            path="/recuperar",
            json_body={
                "correo": correo,
                "nueva_contrasena": nueva_contrasena
            }
        )
