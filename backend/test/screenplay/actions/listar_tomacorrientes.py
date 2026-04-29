from test.screenplay.actions.request import SendRequest


class ListarTomacorrientes:
    def perform_as(self, actor):
        actor.attempts_to(SendRequest("get", "/perfil"))
