from test.screenplay.actions.request import SendRequest

class CambiarEstadoDispositivo(SendRequest):
    def __init__(self, id_dispositivo: int, estado_activo: bool):
        super().__init__(
            method="put",
            path=f"/perfil/dispositivo/{id_dispositivo}/estado",
            json_body={
                "estado_activo": estado_activo
            }
        )
