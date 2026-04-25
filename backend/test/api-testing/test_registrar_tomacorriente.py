import pytest
from unittest.mock import Mock, patch
from hamcrest import assert_that, is_, equal_to, has_length, close_to, none, not_none

with patch("google.genai.Client") as FakeClient:
    fake_models = Mock()
    fake_models.generate_content.return_value = Mock(text="{}")
    FakeClient.return_value = Mock(models=fake_models)
    from app import app
import src.routes.vista_perfil as vp


class hogar_fake:
    def __init__(self, id_hogar: int = 1) -> None:
        self.id_hogar = id_hogar

    def to_dict(self) -> dict:
        return {"id_hogar": self.id_hogar}


class DispositivoFake:
    def __init__(self, id_hogar: int, alias: str, device_id: str) -> None:
        self.id_dispositivos = 123
        self.id_hogar = id_hogar
        self.alias = alias
        self.id_dispositivo_iot = device_id
        self.tipo_dispositivo_ia = None
        self.estado_activo = False
        self.fecha_conexion = None

    def to_dict(self) -> dict:
        return {
            "id_dispositivos": self.id_dispositivos,
            "id_hogar": self.id_hogar,
            "alias": self.alias,
            "id_dispositivo_iot": self.id_dispositivo_iot,
            "tipo_dispositivo_ia": self.tipo_dispositivo_ia,
            "estado_activo": self.estado_activo,
            "fecha_conexion": self.fecha_conexion,
        }


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "testing-secret"
    app.config["SESSION_COOKIE_SECURE"] = False
    with app.test_client() as client:
        with app.app_context():
            yield client


def _seed_session(client) -> None:
    with client.session_transaction() as sess:
        sess["usuario"] = {"id": 42, "correo": "admin@gmail.com"}


@pytest.fixture(autouse=True)
def stub_dispositivos(monkeypatch):
    # Base de datos falsa y llamados a base de datos falsa para testear, y no afectar una base de datos real
    registrados = set()

    def fake_verificar(device_id: str) -> bool:
        return device_id in registrados

    def fake_hogar(_id_usuario: int):
        return hogar_fake(id_hogar=99)

    def fake_crear_dispositivo(id_hogar: int, alias: str, id_dispositivo_iot: str):
        registrados.add(id_dispositivo_iot)
        return DispositivoFake(id_hogar, alias, id_dispositivo_iot)

    monkeypatch.setattr(vp, "verificar_dispositivo_existe", fake_verificar)
    monkeypatch.setattr(vp, "obtener_hogar_por_usuario", fake_hogar)
    monkeypatch.setattr(vp, "crear_dispositivo", fake_crear_dispositivo)

    return {"registrados": registrados}


def test_cp_tom_001_registro_valido(client):
    _seed_session(client)

    resp = client.post("/perfil", json={"deviceId": "TOM001", "nickname": "Nevera"})
    data = resp.get_json()

    assert_that(resp.status_code, is_(equal_to(201)))
    assert_that(data["success"], is_(equal_to(True)))
    assert_that(data["dispositivo"]["alias"], is_(equal_to("Nevera")))
    assert_that(data["dispositivo"]["id_dispositivo_iot"], is_(equal_to("TOM001")))


def test_cp_campos_vacios(client):
    _seed_session(client)
    resp = client.post("/perfil", json={"deviceId": "", "nickname": ""})
    data = resp.get_json()
    assert_that(resp.status_code, is_(equal_to(400)))
    assert_that(data["success"], is_(equal_to(False)))
    assert "requeridos" in data["error"].lower()


def test_cp_id_vacio_apodo_valido(client):
    _seed_session(client)
    resp = client.post("/perfil", json={"deviceId": "", "nickname": "TV Sala"})
    data = resp.get_json()
    assert_that(resp.status_code, is_(equal_to(400)))
    assert_that(data["success"], is_(equal_to(False)))


def test_cp_tom_002_id_valido_apodo_vacio(client):
    _seed_session(client)
    resp = client.post("/perfil", json={"deviceId": "TOM002", "nickname": ""})
    data = resp.get_json()
    assert_that(resp.status_code, is_(equal_to(400)))
    assert_that(data["success"], is_(equal_to(False)))


def test_cp_tom_001_dispositivo_existente(client, monkeypatch):
    _seed_session(client)

    monkeypatch.setattr(vp, "verificar_dispositivo_existe", lambda device_id: device_id == "TOM001")

    resp = client.post("/perfil", json={"deviceId": "TOM001", "nickname": "Microondas"})
    data = resp.get_json()
    assert_that(resp.status_code, is_(equal_to(400)))
    assert_that(data["success"], is_(equal_to(False)))
    assert "ya está registrado" in data["error"].lower()


def test_cp_tom_003_sin_hogar_previo(client, monkeypatch):
    _seed_session(client)
    monkeypatch.setattr(vp, "obtener_hogar_por_usuario", lambda _uid: None)

    resp = client.post("/perfil", json={"deviceId": "TOM003", "nickname": "Lavadora"})
    data = resp.get_json()
    assert_that(resp.status_code, is_(equal_to(400)))
    assert_that(data["success"], is_(equal_to(False)))
    assert "hogar" in data["error"].lower()


def test_cp_tom_004_apodo_muy_largo(client, monkeypatch):
    _seed_session(client)

    def crear_condicional(id_hogar: int, alias: str, id_dispositivo_iot: str):
        if len(alias) > 50:
            return None
        return DispositivoFake(id_hogar, alias, id_dispositivo_iot)

    monkeypatch.setattr(vp, "crear_dispositivo", crear_condicional)

    apodo_largo = "Este es un apodo extremadamente largo que supera los 50 caracteres permitidos por el sistema"
    resp = client.post("/perfil", json={"deviceId": "TOM004", "nickname": apodo_largo})
    data = resp.get_json()
    assert_that(resp.status_code, is_(equal_to(500)))
    assert_that(data["success"], is_(equal_to(False)))

def test_cp_registros_multiples_consecutivos(client, stub_dispositivos):
    _seed_session(client)

    dispositivos = [
        ("TOM005", "Aire Acondicionado"),
        ("TOM006", "Horno"),
        ("TOM007", "Lavadora"),
    ]

    for device_id, alias in dispositivos:
        resp = client.post("/perfil", json={"deviceId": device_id, "nickname": alias})
        assert_that(resp.status_code, is_(equal_to(201)))
        assert_that(resp.get_json()["success"], is_(equal_to(True)))

    assert_that(stub_dispositivos["registrados"], is_(equal_to({"TOM005", "TOM006", "TOM007"})))


def test_cp_tom_008_apodo_caracteres_especiales(client):
    _seed_session(client)
    resp = client.post("/perfil", json={"deviceId": "TOM008", "nickname": "Cargador@Móvil#2024"})
    data = resp.get_json()
    assert_that(resp.status_code, is_(equal_to(201)))
    assert_that(resp.get_json()["success"], is_(equal_to(True)))
    assert_that(data["dispositivo"]["alias"], is_(equal_to("Cargador@Móvil#2024")))


def test_perfil_payload_redirige_a_seleccionar(monkeypatch, client):
    _seed_session(client)
    seleccionar_mock = Mock(return_value=({"success": True, "message": "perfil"}, 200))
    monkeypatch.setattr(vp, "seleccionar_accion_perfil", seleccionar_mock)

    resp = client.post(
        "/perfil",
        json={"address": "Calle 1", "nombre_hogar": "Casa"},
    )

    assert_that(resp.status_code, is_(equal_to(200)))
    assert_that(resp.get_json()["message"], is_(equal_to("perfil")))
    seleccionar_mock.assert_called_once()


def test_payload_invalido_retorna_error(client):
    _seed_session(client)

    resp = client.post("/perfil", json={"foo": "bar"})

    assert_that(resp.status_code, is_(equal_to(400)))
    data = resp.get_json()
    assert_that(data["success"], is_(equal_to(False)))
    assert "no coincide" in data["error"].lower()
