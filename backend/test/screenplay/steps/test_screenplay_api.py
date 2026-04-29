from pytest_bdd import scenarios, given, when, then, parsers

import src.routes.vista_perfil as vp
import src.routes.vista_usuarios as vu

from test.screenplay.actions.login import IniciarSesion
from test.screenplay.actions.logout import CerrarSesion
from test.screenplay.actions.registrar_tomacorriente import RegistrarTomacorriente
from test.screenplay.actions.listar_tomacorrientes import ListarTomacorrientes
from test.screenplay.actions.eliminar_tomacorriente import EliminarTomacorriente
from test.screenplay.actions.session import SeedSession
from test.screenplay.questions.last_response import response_json, response_status


scenarios("../features/login.feature")
scenarios("../features/logout.feature")
scenarios("../features/registrar_tomacorriente.feature")
scenarios("../features/listar_tomacorrientes.feature")
scenarios("../features/eliminar_tomacorriente.feature")


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


@when(parsers.parse("inicia sesion con correo \"{correo}\" y contrasena \"{contrasena}\""))
def inicia_sesion(actor, correo, contrasena):
    actor.attempts_to(IniciarSesion(correo, contrasena))


@when("cierra sesion")
def cierra_sesion(actor):
    actor.attempts_to(CerrarSesion())


@when(parsers.parse("registra tomacorriente con id \"{device_id}\" y apodo \"{nickname}\""))
def registra_tomacorriente(actor, device_id, nickname):
    actor.attempts_to(RegistrarTomacorriente(device_id, nickname))


@when("lista tomacorrientes")
def lista_tomacorrientes(actor):
    actor.attempts_to(ListarTomacorrientes())


@when(parsers.parse("elimina el tomacorriente con id {dispositivo_id:d}"))
def elimina_tomacorriente(actor, dispositivo_id):
    actor.attempts_to(EliminarTomacorriente(dispositivo_id))


@then(parsers.parse("la respuesta es exitosa con codigo {codigo:d}"))
def respuesta_exitosa(actor, codigo):
    assert response_status(actor) == codigo


@then(parsers.parse("el correo del usuario en respuesta es \"{correo}\""))
def correo_respuesta(actor, correo):
    data = response_json(actor)
    assert data["usuario"]["correo"] == correo


@then(parsers.parse("el tomacorriente registrado tiene apodo \"{nickname}\""))
def apodo_registrado(actor, nickname):
    data = response_json(actor)
    assert data["dispositivo"]["alias"] == nickname


@then(parsers.parse("se listan {cantidad:d} tomacorrientes"))
def lista_con_cantidad(actor, cantidad):
    data = response_json(actor)
    assert len(data["dispositivos"]) == cantidad
