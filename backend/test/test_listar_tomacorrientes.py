import pytest
from unittest.mock import Mock, patch

with patch("google.genai.Client") as FakeClient:
    fake_models = Mock()
    fake_models.generate_content.return_value = Mock(text="{}")
    FakeClient.return_value = Mock(models=fake_models)
    from app import app
import src.routes.vista_perfil as vp


class HogarFake:
    def __init__(self, id_hogar: int, nombre: str = "Mi Hogar", direccion: str = "Calle 123") -> None:
        self.id_hogar = id_hogar
        self.nombre_hogar = nombre
        self.direccion = direccion

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


def _seed_session(client) -> None:
    with client.session_transaction() as sess:
        sess["usuario"] = {"id": 7, "correo": "user@test.com"}


def _set_hogar_stub(monkeypatch):
    monkeypatch.setattr(vp, "obtener_hogar_por_usuario", lambda uid: HogarFake(id_hogar=99))


def _set_devices(monkeypatch, devices: list[DispositivoFake]):
    monkeypatch.setattr(vp, "obtener_dispositivos_por_usuario", lambda _uid: devices)


# -------------------------------------------------
# Casos de listado de tomacorrientes
# -------------------------------------------------


def test_cp_list_001_lista_con_dispositivos(client, monkeypatch):
    _seed_session(client)
    _set_hogar_stub(monkeypatch)
    _set_devices(
        monkeypatch,
        [DispositivoFake(1, "Cargador", False), DispositivoFake(2, "Lavadora", True)],
    )

    resp = client.get("/perfil")
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["success"] is True
    nombres_dispositivos_en_data = [d["alias"] for d in data["dispositivos"]]
    assert nombres_dispositivos_en_data == ["Cargador", "Lavadora"]


def test_cp_list_002_lista_vacia(client, monkeypatch):
    _seed_session(client)
    _set_hogar_stub(monkeypatch)
    _set_devices(monkeypatch, [])

    resp = client.get("/perfil")
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["success"] is True
    assert data["dispositivos"] == []


def test_cp_list_003_estado_desconectado(client, monkeypatch):
    _seed_session(client)
    _set_hogar_stub(monkeypatch)
    _set_devices(monkeypatch, [DispositivoFake(1, "Cargador", False)])

    resp = client.get("/perfil")
    data = resp.get_json()
    assert data["dispositivos"][0]["estado_activo"] is False


def test_cp_list_004_estado_conectado(client, monkeypatch):
    _seed_session(client)
    _set_hogar_stub(monkeypatch)
    _set_devices(monkeypatch, [DispositivoFake(2, "Lavadora", True)])

    resp = client.get("/perfil")
    data = resp.get_json()
    assert data["dispositivos"][0]["estado_activo"] is True


def test_cp_list_005_verificar_campos_correctos(client, monkeypatch):
    _seed_session(client)
    _set_hogar_stub(monkeypatch)
    device = DispositivoFake(3, "Microondas", True)
    _set_devices(monkeypatch, [device])

    resp = client.get("/perfil")
    data = resp.get_json()
    device_json = data["dispositivos"][0]

    assert device_json["id_dispositivos"] == 3
    assert device_json["alias"] == "Microondas"


def test_cp_list_006_actualiza_lista_despues_de_registro(client, monkeypatch):
    _seed_session(client)
    _set_hogar_stub(monkeypatch)

    devices: list[DispositivoFake] = [DispositivoFake(4, "TV", True)]
    _set_devices(monkeypatch, devices)

    first = client.get("/perfil").get_json()
    assert len(first["dispositivos"]) == 1

    # Agregamos otro dispositivo
    devices.append(DispositivoFake(5, "Aire", False))
    second = client.get("/perfil").get_json()
    assert len(second["dispositivos"]) == 2


def test_cp_list_007_lista_multiple(client, monkeypatch):
    _seed_session(client)
    _set_hogar_stub(monkeypatch)
    muchos_dispositivos = [DispositivoFake(i, f"Dispositivo-{i}", False) for i in range(1, 7)]
    _set_devices(monkeypatch, muchos_dispositivos)

    data = client.get("/perfil").get_json()
    assert len(data["dispositivos"]) >= 5


def test_cp_list_008_refresh_persistente(client, monkeypatch):
    _seed_session(client)
    _set_hogar_stub(monkeypatch)
    devices = [DispositivoFake(10, "Cafetera", True)]
    _set_devices(monkeypatch, devices)

    first = client.get("/perfil").get_json()["dispositivos"]
    second = client.get("/perfil").get_json()["dispositivos"]
    assert first == second
