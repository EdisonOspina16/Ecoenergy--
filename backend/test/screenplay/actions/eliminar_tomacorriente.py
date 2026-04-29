from test.screenplay.actions.request import SendRequest


class EliminarTomacorriente:
    def __init__(self, dispositivo_id: int):
        self.dispositivo_id = dispositivo_id

    def perform_as(self, actor):
        actor.attempts_to(SendRequest("delete", f"/perfil/dispositivo/{self.dispositivo_id}"))
