from test.screenplay.actions.request import SendRequest


class SolicitarRecomendacion:
    """
    Tarea Screenplay: solicitar una recomendacion de ahorro energetico
    para un dispositivo especifico con su consumo en watts.
    Endpoint: POST /recomendacion
    """

    def __init__(self, dispositivo: str, consumo_watts: float):
        self.dispositivo = dispositivo
        self.consumo_watts = consumo_watts

    def perform_as(self, actor):
        actor.attempts_to(
            SendRequest(
                "post",
                "/recomendacion",
                {
                    "dispositivo": self.dispositivo,
                    "consumo_watts": self.consumo_watts,
                },
            )
        )


class SolicitarRecomendacionSinDatos:
    """
    Tarea Screenplay: solicitar una recomendacion sin datos validos
    para verificar el manejo de errores del endpoint.
    """

    def perform_as(self, actor):
        actor.attempts_to(
            SendRequest(
                "post",
                "/recomendacion",
                {"dispositivo": None, "consumo_watts": None},
            )
        )
