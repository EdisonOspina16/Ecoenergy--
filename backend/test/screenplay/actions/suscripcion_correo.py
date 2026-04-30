from test.screenplay.actions.request import SendRequest

class SuscripcionCorreo(SendRequest):
    def __init__(self, email: str):
        super().__init__(
            method="post",
            path="/subscribe",
            json_body={
                "email": email
            }
        )
