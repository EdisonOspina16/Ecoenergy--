from test.screenplay.actors.abilities import ApiClient


class SeedSession:
    def __init__(self, usuario: dict):
        self.usuario = usuario

    def perform_as(self, actor):
        client = actor.ability_to(ApiClient).client
        with client.session_transaction() as sess:
            sess["usuario"] = self.usuario
