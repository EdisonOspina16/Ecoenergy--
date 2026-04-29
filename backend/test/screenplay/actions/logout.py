from test.screenplay.actions.request import SendRequest


class CerrarSesion:
    def perform_as(self, actor):
        actor.attempts_to(SendRequest("post", "/logout"))
