import pytest
from unittest.mock import Mock, patch
from hamcrest import assert_that, is_, equal_to

with patch("google.genai.Client") as FakeClient:
    fake_models = Mock()
    fake_models.generate_content.return_value = Mock(text="{}")
    FakeClient.return_value = Mock(models=fake_models)
    from app import app
import src.routes.vista_perfil as vp


class HogarFake:
    def __init__(self, id_hogar: int = 99) -> None:
        self.id_hogar = id_hogar
        self.nombre_hogar = "Mi Hogar"
        self.direccion = "Calle 123"

    def to_dict(self) -> dict:
        return {
            "id_hogar": self.id_hogar,
            "nombre_hogar": self.nombre_hogar,
            "direccion": self.direccion,
        }


class DispositivoFake:
    def __init__(self, id_dispositivos: int, alias: str, estado_activo: bool) -> None:
        self.id_dispositivos = id_dispositivos
        self.id_hogar = 99
        self.alias = alias
        self.id_dispositivo_iot = f"ID-{id_dispositivos}"
        self.tipo_dispositivo_ia = None
        self.estado_activo = estado_activo
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


def _seed_session(client):
    with client.session_transaction() as sess:
        sess["usuario"] = {"id": 7, "correo": "user@test.com"}


@pytest.fixture()
def dispositivo_state(monkeypatch):
    devices: dict[int, DispositivoFake] = {}

    def set_devices(items: list[DispositivoFake]):
        devices.clear()
        devices.update({d.id_dispositivos: d for d in items})

    def fake_hogar(_uid: int):
        return HogarFake()

    def fake_listar(_uid: int):
        return list(devices.values())

    def fake_eliminar(id_dispositivo: int, _uid: int):
        if id_dispositivo in devices:
            devices.pop(id_dispositivo)
            return True
        return False

    monkeypatch.setattr(vp, "obtener_hogar_por_usuario", fake_hogar)
    monkeypatch.setattr(vp, "obtener_dispositivos_por_usuario", fake_listar)
    monkeypatch.setattr(vp, "eliminar_dispositivo", fake_eliminar)

    return {"devices": devices, "set_devices": set_devices}


def test_eliminar_desconectado(client, dispositivo_state):
    _seed_session(client)
    dispositivo_state["set_devices"]([DispositivoFake(1, "Lavadora", False)])

    resp = client.delete("/perfil/dispositivo/1")
    data = resp.get_json()

    assert_that(resp.status_code, is_(equal_to(200)))
    assert_that(data["success"], is_(equal_to(True)))
    assert "eliminado" in data["message"].lower()


def test_eliminar_conectado(client, dispositivo_state):
    _seed_session(client)
    dispositivo_state["set_devices"]([DispositivoFake(2, "Lavadora", True)])

    resp = client.delete("/perfil/dispositivo/2")
    assert_that(resp.status_code, is_(equal_to(200)))
    assert_that(resp.get_json()["success"], is_(equal_to(True)))


def test_mensaje_exito(client, dispositivo_state):
    _seed_session(client)
    dispositivo_state["set_devices"]([DispositivoFake(3, "Lavadora", True)])

    resp = client.delete("/perfil/dispositivo/3")
    assert "exitosamente" in resp.get_json()["message"].lower()


def test_no_aparece_al_recargar(client, dispositivo_state):
    _seed_session(client)
    dispositivo_state["set_devices"]([
        DispositivoFake(4, "Lavadora", False),
        DispositivoFake(5, "TV", True),
    ])

    client.delete("/perfil/dispositivo/4")
    data = client.get("/perfil").get_json()
    aliases = [d["alias"] for d in data["dispositivos"]]

    assert "Lavadora" not in aliases
    assert "TV" in aliases


def test_eliminar_clicks_rapidos(client, dispositivo_state):
    _seed_session(client)
    dispositivo_state["set_devices"]([DispositivoFake(7, "Lavadora", False)])

    first = client.delete("/perfil/dispositivo/7")
    second = client.delete("/perfil/dispositivo/7")

    assert_that(first.status_code, is_(equal_to(200)))
    assert_that(second.status_code, is_(equal_to(404)))


def test_eliminar_sin_dispositivos(client, dispositivo_state):
    _seed_session(client)
    dispositivo_state["set_devices"]([])

    resp = client.delete("/perfil/dispositivo/8")
    assert_that(resp.status_code, is_(equal_to(404)))
    assert_that(resp.get_json()["success"], is_(equal_to(False)))


def test_no_aparece_despues_de_eliminar(client, dispositivo_state):
    _seed_session(client)
    dispositivo_state["set_devices"]([DispositivoFake(9, "Lavadora", True)])

    client.delete("/perfil/dispositivo/9")
    data = client.get("/perfil").get_json()

    assert "Lavadora" not in [d["alias"] for d in data["dispositivos"]]

    assert_that(data["success"], is_(equal_to(True)))


def test_eliminar_dispositivo_error_500(monkeypatch, client):
    # Arrange
    _seed_session(client)
    error = RuntimeError("fallo eliminando")
    eliminar_mock = Mock(side_effect=error)
    monkeypatch.setattr(vp, "eliminar_dispositivo", eliminar_mock)

    # Act
    resp = client.delete("/perfil/dispositivo/123")
    data = resp.get_json()

    # Assert
    assert_that(resp.status_code, is_(equal_to(500)))
    assert_that(data["success"], is_(equal_to(False)))
    assert "fallo eliminando" in data["error"]
    eliminar_mock.assert_called_once_with(123, 7)
