from test.screenplay.actions.request import SendRequest


class GenerarRecomendacionDiaria:
    """
    Tarea Screenplay: generar y guardar la recomendacion diaria del hogar,
    que incluye:
      - recomendaciones por dispositivo (llamar_recomendacion)
      - ahorro financiero estimado      (llamar_ahorro_estimado)
      - impacto ambiental               (llamar_ahorro_estimado)
      - indicador didactico / huella de carbono (llamar_ahorro_estimado)
    Endpoint: POST /recomendacion-diaria/generar
    """

    def perform_as(self, actor):
        actor.attempts_to(
            SendRequest("post", "/recomendacion-diaria/generar")
        )


class ConsultarRecomendacionDiaria:
    """
    Tarea Screenplay: obtener la recomendacion diaria del hogar ya guardada.
    Endpoint: GET /recomendacion-diaria
    """

    def perform_as(self, actor):
        actor.attempts_to(
            SendRequest("get", "/recomendacion-diaria")
        )


class ConsultarAhorroEstimado:
    """
    Tarea Screenplay: consultar el ahorro estimado global (todos los dispositivos).
    Incluye ahorro financiero, impacto ambiental e indicador de huella de carbono.
    Endpoint: GET /ahorro-estimado
    """

    def perform_as(self, actor):
        actor.attempts_to(
            SendRequest("get", "/ahorro-estimado")
        )
