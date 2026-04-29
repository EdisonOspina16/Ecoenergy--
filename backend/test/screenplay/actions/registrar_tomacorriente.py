from test.screenplay.actions.request import SendRequest


class RegistrarTomacorriente:
    def __init__(self, device_id: str, nickname: str):
        self.device_id = device_id
        self.nickname = nickname

    def perform_as(self, actor):
        actor.attempts_to(
            SendRequest(
                "post",
                "/perfil",
                {"deviceId": self.device_id, "nickname": self.nickname},
            )
        )
