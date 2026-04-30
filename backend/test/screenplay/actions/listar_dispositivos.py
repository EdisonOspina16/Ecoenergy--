from test.screenplay.actions.request import SendRequest

class ListarDispositivos(SendRequest):
    def __init__(self):
        super().__init__(
            method="get",
            path="/dispositivos"
        )
