from test.screenplay.actions.request import SendRequest

class CrearPerfilHogar(SendRequest):
    def __init__(self, direccion: str, nombre_hogar: str):
        super().__init__(
            method="post",
            path="/perfil",
            json_body={
                "address": direccion,
                "nombre_hogar": nombre_hogar
            }
        )
