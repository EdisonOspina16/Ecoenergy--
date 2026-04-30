from pytest_bdd import scenarios, given, when, then, parsers

import src.routes.vista_perfil as vp
import src.routes.vista_usuarios as vu
import src.aplication.service.consumo_service as cs
import src.aplication.service.usuario_service as us

from test.screenplay.actions.login import IniciarSesion
from test.screenplay.actions.logout import CerrarSesion
from test.screenplay.actions.registrar_tomacorriente import RegistrarTomacorriente
from test.screenplay.actions.listar_tomacorrientes import ListarTomacorrientes
from test.screenplay.actions.eliminar_tomacorriente import EliminarTomacorriente
from test.screenplay.actions.registrar_usuario import RegistrarUsuario, RegistrarUsuarioSinCampos
from test.screenplay.actions.generar_recomendacion import SolicitarRecomendacion, SolicitarRecomendacionSinDatos
from test.screenplay.actions.ahorro_impacto_huella import (
    GenerarRecomendacionDiaria,
    ConsultarRecomendacionDiaria,
    ConsultarAhorroEstimado,
)
from test.screenplay.actions.session import SeedSession
from test.screenplay.questions.last_response import response_json, response_status


# ---------------------------------------------------------------------------
# Registro de escenarios por feature
# ---------------------------------------------------------------------------
scenarios("../features/login.feature")
scenarios("../features/logout.feature")
scenarios("../features/registrar_tomacorriente.feature")
scenarios("../features/listar_tomacorrientes.feature")
scenarios("../features/eliminar_tomacorriente.feature")
scenarios("../features/registrar_usuario.feature")
scenarios("../features/generar_recomendaciones.feature")
scenarios("../features/ahorro_impacto_huella.feature")


# ===========================================================================
# STUBS reutilizables
# ===========================================================================

class UsuarioStub:
    def __init__(self, correo: str):
        self.correo = correo

    def to_dict(self):
        return {
            "id": 1,
            "nombre": "Test",
            "apellidos": "User",
            "correo": self.correo,
        }


class HogarStub:
    def __init__(self, id_hogar: int = 99):
        self.id_hogar = id_hogar

    def to_dict(self):
        return {"id_hogar": self.id_hogar}


class DispositivoStub:
    def __init__(self, id_dispositivos: int, alias: str, estado_activo: bool):
        self.id_dispositivos = id_dispositivos
        self.id_hogar = 99
        self.alias = alias
        self.id_dispositivo_iot = f"ID-{id_dispositivos}"
        self.tipo_dispositivo_ia = None
        self.estado_activo = estado_activo
        self.fecha_conexion = None

    def to_dict(self):
        return {
            "id_dispositivos": self.id_dispositivos,
            "id_hogar": self.id_hogar,
            "alias": self.alias,
            "id_dispositivo_iot": self.id_dispositivo_iot,
            "tipo_dispositivo_ia": self.tipo_dispositivo_ia,
            "estado_activo": self.estado_activo,
            "fecha_conexion": self.fecha_conexion,
        }


# ===========================================================================
# STEPS — FEATURES EXISTENTES (login / logout / tomacorriente)
# ===========================================================================

@given("el actor tiene credenciales validas")
def credenciales_validas(monkeypatch):
    def verificar(correo: str, contrasena: str):
        return UsuarioStub(correo)

    monkeypatch.setattr(vu, "verificar_credenciales", verificar)


@given("el actor tiene una sesion activa")
def sesion_activa(actor):
    actor.attempts_to(SeedSession({"id": 7, "correo": "user@test.com"}))


@given("el hogar existe y el dispositivo no esta registrado")
def hogar_y_dispositivo_stub(monkeypatch):
    monkeypatch.setattr(vp, "obtener_hogar_por_usuario", lambda _uid: HogarStub())
    monkeypatch.setattr(vp, "verificar_dispositivo_existe", lambda _device_id: False)

    def crear_dispositivo(id_hogar: int, alias: str, id_dispositivo_iot: str):
        return DispositivoStub(1, alias, False)

    monkeypatch.setattr(vp, "crear_dispositivo", crear_dispositivo)


@given("existen tomacorrientes registrados")
def tomacorrientes_registrados(monkeypatch, actor):
    dispositivos = [DispositivoStub(1, "Cargador", False), DispositivoStub(2, "Lavadora", True)]
    monkeypatch.setattr(vp, "obtener_hogar_por_usuario", lambda _uid: HogarStub())
    monkeypatch.setattr(vp, "obtener_dispositivos_por_usuario", lambda _uid: dispositivos)
    actor.remember("dispositivos", dispositivos)


@given(parsers.parse("existe el tomacorriente con id {dispositivo_id:d}"))
def tomacorriente_existe(monkeypatch, dispositivo_id):
    dispositivos = {dispositivo_id: DispositivoStub(dispositivo_id, "Lavadora", False)}

    def listar(_uid: int):
        return list(dispositivos.values())

    def eliminar(id_dispositivo: int, _uid: int):
        return dispositivos.pop(id_dispositivo, None) is not None

    monkeypatch.setattr(vp, "obtener_hogar_por_usuario", lambda _uid: HogarStub())
    monkeypatch.setattr(vp, "obtener_dispositivos_por_usuario", listar)
    monkeypatch.setattr(vp, "eliminar_dispositivo", eliminar)


# ===========================================================================
# STEPS — REGISTRAR USUARIO
# ===========================================================================

@given("el usuario no esta registrado en el sistema")
def usuario_no_registrado(monkeypatch):
    """
    Stub del servicio de registro para simular un registro exitoso sin BD.
    Se parchea en el módulo vista_usuarios (vu) donde está la referencia
    local, igual que se hace con verificar_credenciales en el login.
    """
    monkeypatch.setattr(vu, "registrar_usuario", lambda **kwargs: True)


@when(
    parsers.parse(
        'registra una cuenta con nombre "{nombre}" apellidos "{apellidos}" '
        'correo "{correo}" y contrasena "{contrasena}"'
    )
)
def registra_usuario(actor, nombre, apellidos, correo, contrasena):
    actor.attempts_to(RegistrarUsuario(nombre, apellidos, correo, contrasena))


@when("intenta registrarse sin proporcionar todos los campos requeridos")
def registra_usuario_sin_campos(actor):
    actor.attempts_to(RegistrarUsuarioSinCampos())


# ===========================================================================
# STEPS — GENERAR RECOMENDACIONES DE AHORRO
# ===========================================================================

@when(
    parsers.parse(
        'solicita recomendacion para el dispositivo "{dispositivo}" con consumo de {consumo:d} watts'
    )
)
def solicita_recomendacion(actor, dispositivo, consumo, monkeypatch):
    """Stub de llamar_recomendacion para no llamar a Gemini en tests."""
    monkeypatch.setattr(
        cs,
        "llamar_recomendacion",
        lambda watts, disp: f"Recomendacion stub para {disp}",
    )
    actor.attempts_to(SolicitarRecomendacion(dispositivo, float(consumo)))


@when("solicita recomendacion sin datos del dispositivo")
def solicita_recomendacion_sin_datos(actor, monkeypatch):
    """Stub que lanza excepcion para cubrir la rama de error del endpoint."""
    monkeypatch.setattr(
        cs,
        "llamar_recomendacion",
        lambda watts, disp: (_ for _ in ()).throw(Exception("Datos invalidos")),
    )
    actor.attempts_to(SolicitarRecomendacionSinDatos())


# ===========================================================================
# STEPS — AHORRO ECONOMICO / IMPACTO AMBIENTAL / HUELLA DE CARBONO
# ===========================================================================

_AHORRO_STUB = {
    "ahorro_financiero": "Puedes ahorrar $25.000 COP/mes",
    "impacto_ambiental": "Reduccion de 3.2 kg CO2 al mes",
    "indicador_didactico": "Equivale a plantar 1 arbol al mes",
}

_RECOMENDACION_DIARIA_STUB = {
    "encontrado": True,
    "recomendaciones": [
        {
            "dispositivo": "Nevera",
            "recomendacion": "Mantén la nevera a 4°C para un consumo óptimo.",
            "esAlerta": False,
        }
    ],
    "ahorro_financiero": _AHORRO_STUB["ahorro_financiero"],
    "impacto_ambiental": _AHORRO_STUB["impacto_ambiental"],
    "indicador_didactico": _AHORRO_STUB["indicador_didactico"],
}


@given("existen dispositivos con consumo registrado para el usuario")
def dispositivos_con_consumo_usuario(monkeypatch):
    """
    Stub: simula dispositivos del usuario y el hogar para que
    generar_y_guardar_recomendacion_diaria funcione sin BD.
    Parchea las referencias importadas dentro del módulo consumo_service.
    """
    hogar = HogarStub(id_hogar=99)
    dispositivos_lista = [
        {"nombre": "Nevera", "consumo_watts": 150.0},
        {"nombre": "Lavadora", "consumo_watts": 500.0},
    ]
    # Parchea la función interna que abre conexión BD
    monkeypatch.setattr(cs, "_obtener_hogar", lambda uid: hogar)
    # Parchea la referencia local del módulo (no el repositorio original)
    monkeypatch.setattr(cs, "obtener_dispositivos_por_usuario", lambda uid: dispositivos_lista)


@given("la IA genera datos de ahorro estimado con impacto ambiental y huella de carbono")
def ia_stub_ahorro(monkeypatch):
    """
    Stub de llamar_recomendacion y llamar_ahorro_estimado para no
    invocar la API de Gemini durante los tests.
    Parchea las referencias importadas dentro del módulo consumo_service.
    """
    # Stubea el cliente de IA (refs. locales en consumo_service)
    monkeypatch.setattr(cs, "llamar_recomendacion", lambda watts, disp: f"Recomendacion stub para {disp}")
    monkeypatch.setattr(cs, "llamar_ahorro_estimado", lambda dispositivos: _AHORRO_STUB)
    # Stubea las funciones de repositorio usando su referencia en consumo_service
    monkeypatch.setattr(cs, "guardar_recomendacion_diaria", lambda id_hogar, recs, ahorro: None)
    monkeypatch.setattr(cs, "obtener_recomendacion_diaria", lambda id_hogar: None)


@given("existe una recomendacion diaria guardada para el hogar del usuario")
def recomendacion_diaria_guardada(monkeypatch):
    """Stub: simula que ya hay una recomendacion diaria persistida."""
    hogar = HogarStub(id_hogar=99)
    monkeypatch.setattr(cs, "_obtener_hogar", lambda uid: hogar)
    # Parchea la ref. local del módulo consumo_service
    monkeypatch.setattr(cs, "obtener_recomendacion_diaria", lambda id_hogar: _RECOMENDACION_DIARIA_STUB)


@given("existen dispositivos globales con consumo registrado")
def dispositivos_globales(monkeypatch):
    """Stub de la consulta de dispositivos globales para /ahorro-estimado."""
    dispositivos_lista = [
        {"nombre": "Nevera", "consumo_watts": 150.0},
        {"nombre": "Televisor", "consumo_watts": 100.0},
    ]
    # Parchea la referencia local del módulo consumo_service
    monkeypatch.setattr(cs, "obtener_dispositivos_con_ultimo_consumo", lambda: dispositivos_lista)
    monkeypatch.setattr(cs, "llamar_ahorro_estimado", lambda dispositivos: _AHORRO_STUB)


@when("genera la recomendacion diaria del hogar")
def genera_recomendacion_diaria(actor):
    actor.attempts_to(GenerarRecomendacionDiaria())


@when("consulta la recomendacion diaria del hogar")
def consulta_recomendacion_diaria(actor):
    actor.attempts_to(ConsultarRecomendacionDiaria())


@when("consulta el ahorro estimado global")
def consulta_ahorro_estimado(actor):
    actor.attempts_to(ConsultarAhorroEstimado())


# ===========================================================================
# STEPS — WHEN (features existentes)
# ===========================================================================

@when(parsers.parse('inicia sesion con correo "{correo}" y contrasena "{contrasena}"'))
def inicia_sesion(actor, correo, contrasena):
    actor.attempts_to(IniciarSesion(correo, contrasena))


@when("cierra sesion")
def cierra_sesion(actor):
    actor.attempts_to(CerrarSesion())


@when(parsers.parse('registra tomacorriente con id "{device_id}" y apodo "{nickname}"'))
def registra_tomacorriente(actor, device_id, nickname):
    actor.attempts_to(RegistrarTomacorriente(device_id, nickname))


@when("lista tomacorrientes")
def lista_tomacorrientes(actor):
    actor.attempts_to(ListarTomacorrientes())


@when(parsers.parse("elimina el tomacorriente con id {dispositivo_id:d}"))
def elimina_tomacorriente(actor, dispositivo_id):
    actor.attempts_to(EliminarTomacorriente(dispositivo_id))


# ===========================================================================
# STEPS — THEN compartidos
# ===========================================================================

@then(parsers.parse("la respuesta es exitosa con codigo {codigo:d}"))
def respuesta_exitosa(actor, codigo):
    assert response_status(actor) == codigo


@then(parsers.parse("la respuesta falla con codigo {codigo:d}"))
def respuesta_falla(actor, codigo):
    assert response_status(actor) == codigo


@then(parsers.parse('el correo del usuario en respuesta es "{correo}"'))
def correo_respuesta(actor, correo):
    data = response_json(actor)
    assert data["usuario"]["correo"] == correo


@then(parsers.parse('el tomacorriente registrado tiene apodo "{nickname}"'))
def apodo_registrado(actor, nickname):
    data = response_json(actor)
    assert data["dispositivo"]["alias"] == nickname


@then(parsers.parse("se listan {cantidad:d} tomacorrientes"))
def lista_con_cantidad(actor, cantidad):
    data = response_json(actor)
    assert len(data["dispositivos"]) == cantidad


# --- Registro de usuario ---

@then("el mensaje de respuesta indica registro exitoso")
def mensaje_registro_exitoso(actor):
    data = response_json(actor)
    assert "message" in data
    assert "registrado" in data["message"].lower()


# --- Recomendaciones de ahorro ---

@then(parsers.parse('la respuesta contiene una recomendacion para el dispositivo "{dispositivo}"'))
def recomendacion_para_dispositivo(actor, dispositivo):
    data = response_json(actor)
    assert "recomendacion" in data
    assert "dispositivo" in data
    assert data["dispositivo"] == dispositivo


# --- Ahorro económico / Impacto ambiental / Huella de carbono ---

@then(parsers.parse('la respuesta contiene el campo "{campo}"'))
def respuesta_contiene_campo(actor, campo):
    data = response_json(actor)
    assert campo in data, f"Campo '{campo}' no encontrado en la respuesta: {data}"


@then("la recomendacion diaria fue encontrada")
def recomendacion_diaria_encontrada(actor):
    data = response_json(actor)
    assert data.get("encontrado") is True


@then(parsers.parse('el resultado de ahorro contiene "{campo}"'))
def resultado_ahorro_contiene_campo(actor, campo):
    data = response_json(actor)
    assert "data" in data, f"'data' no encontrado en la respuesta: {data}"
    assert campo in data["data"], (
        f"Campo '{campo}' no encontrado en data: {data['data']}"
    )
