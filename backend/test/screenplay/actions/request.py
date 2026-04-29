from test.screenplay.actors.abilities import ApiClient


class SendRequest:
    def __init__(self, method: str, path: str, json_body=None):
        self.method = method
        self.path = path
        self.json_body = json_body

    def perform_as(self, actor):
        client = actor.ability_to(ApiClient).client
        method = getattr(client, self.method.lower())
        if self.json_body is not None:
            response = method(self.path, json=self.json_body)
        else:
            response = method(self.path)
        actor.remember("response", response)
