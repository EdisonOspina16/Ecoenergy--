import pytest
from unittest.mock import Mock, patch
from hamcrest import assert_that, is_, equal_to, has_length, close_to, none, not_none

with patch("google.genai.Client") as FakeClient:
    fake_models = Mock()
    fake_models.generate_content.return_value = Mock(text="{}")
    FakeClient.return_value = Mock(models=fake_models)
    from app import app


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "testing-secret"
    app.config["SESSION_COOKIE_SECURE"] = False
    with app.test_client() as client:
        with app.app_context():
            yield client


def _seed_session(client):
    # Crea una sesión con usuario autenticado
    with client.session_transaction() as sess:
        sess["usuario"] = {"id": 1, "correo": "admin@gmail.com"}


def test_logout_vacia_sin_sesion(client):
    resp = client.post("/logout")
    assert_that(resp.status_code, is_(equal_to(200)))
    data = resp.get_json()
    assert_that(data["success"], is_(equal_to(True)))
    with client.session_transaction() as sess:
        assert "usuario" not in sess


def test_logout_con_sesion_la_limpia(client):
    _seed_session(client)

    resp = client.post("/logout")
    assert_that(resp.status_code, is_(equal_to(200)))
    data = resp.get_json()
    assert_that(data["success"], is_(equal_to(True)))

    with client.session_transaction() as sess:
        assert "usuario" not in sess


def test_logout_es_idempotente(client):
    # Primera vez con sesión
    _seed_session(client)
    first = client.post("/logout")
    assert_that(first.status_code, is_(equal_to(200)))

    # Segunda vez sin sesión: se sigue devolviendo 200
    second = client.post("/logout")
    assert_that(second.status_code, is_(equal_to(200)))
    data = second.get_json()
    assert_that(data["success"], is_(equal_to(True)))


def test_no_acceso_perfil_tras_logout(client):
    _seed_session(client)
    # se cierra sesión
    client.post("/logout")

    # el intento de acceder a /perfil debe dar 401
    resp = client.get("/perfil")
    assert_that(resp.status_code, is_(equal_to(401)))
    data = resp.get_json()
    assert_that(data["error"])


@pytest.mark.parametrize("veces", [1, 2, 3], ids=lambda v: f"CP-LOG-idempotente-x{v}")
def test_logout_repetido_idempotente(client, veces):
    _seed_session(client)

    for _ in range(veces):
        resp = client.post("/logout")
        assert_that(resp.status_code, is_(equal_to(200)))
        assert_that(resp.get_json()["success"], is_(equal_to(True)))

    with client.session_transaction() as sess:
        assert "usuario" not in sess


def test_logout_y_luego_perfil_y_luego_logout(client):
    """
    Simula: logout, luego intentar entrar en perfil (401), luego logout otra vez (idempotente).
    Cubre los casos "cerrar sesión", "botón atrás/refresh" y "cerrar sesión múltiples veces".
    """
    _seed_session(client)

    # Logout inicial
    first = client.post("/logout")
    assert_that(first.status_code, is_(equal_to(200)))

    # Intento de acceder a /perfil después de hacer logout
    resp_perfil = client.get("/perfil")
    assert_that(resp_perfil.status_code, is_(equal_to(401)))

    # Segundo logout (sin sesión)
    second = client.post("/logout")
    assert_that(second.status_code, is_(equal_to(200)))
    assert_that(second.get_json()["success"], is_(equal_to(True)))


def test_logout_no_rehabilita_sesion_en_refresh(client):
    """Después de hacer logout, una nuevo request sigue sin sesión (aqui simulamos un refresh o un back)."""
    _seed_session(client)
    client.post("/logout")

    # un Refresh con un GET público o vacío (/) no debe recrear usuario en sesión
    resp_root = client.get("/")
    assert_that(resp_root.status_code, is_(equal_to(404)))
    with client.session_transaction() as sess:
        assert "usuario" not in sess
