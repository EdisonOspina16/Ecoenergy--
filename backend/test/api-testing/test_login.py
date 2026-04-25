import pytest
from unittest.mock import Mock, patch
from hamcrest import assert_that, is_, equal_to

with patch("google.genai.Client") as FakeClient:
    fake_models = Mock()
    fake_models.generate_content.return_value = Mock(text="{}")
    FakeClient.return_value = Mock(models=fake_models)
    from app import app


class UsuarioPrueba:
    def __init__(self, correo="usuario@ejemplo.com"):
        self.correo = correo

    def to_dict(self):
        return {
            "id": 1,
            "nombre": "Test",
            "apellidos": "User",
            "correo": self.correo,
        }


@pytest.fixture()
def client():
    # Testeamos que el cliente tenga soporte de la sesión
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "testing-secret"
    app.config["SESSION_COOKIE_SECURE"] = False
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_login_sin_contrasena(client):
    resp = client.post("/login", json={"correo": "solo@mail.com"})

    assert_that(resp.status_code, is_(equal_to(400)))
    data = resp.get_json()
    assert_that(data["error"], is_(equal_to("Faltan campos requeridos")))


def test_login_sin_contrasena_no_llama_verificar(monkeypatch, client):
    verificar_mock = Mock(return_value=None)
    monkeypatch.setattr(
        "src.routes.vista_usuarios.verificar_credenciales",
        verificar_mock,
    )

    resp = client.post("/login", json={"correo": "solo@mail.com"})

    assert_that(resp.status_code, is_(equal_to(400)))
    verificar_mock.assert_not_called()

def test_login_correo_vacio(client):
    resp = client.post("/login", json={"correo": ""})

    assert_that(resp.status_code, is_(equal_to(400)))
    data = resp.get_json()
    assert_that(data["error"], is_(equal_to("Faltan campos requeridos")))


def test_login_credenciales_invalidas(monkeypatch, client):
    # Arrange
    verificar_mock = Mock(return_value=None)
    monkeypatch.setattr(
        "src.routes.vista_usuarios.verificar_credenciales",
        verificar_mock,
    )

    # Act
    resp = client.post(
        "/login",
        json={"correo": "usuario@ejemplo.com", "contrasena": "WrongPass1!"},
    )

    # Assert
    assert_that(resp.status_code, is_(equal_to(401)))
    data = resp.get_json()
    assert_that(data["error"], is_(equal_to("Credenciales inválidas")))
    verificar_mock.assert_called_once_with("usuario@ejemplo.com", "WrongPass1!")
    with client.session_transaction() as sess:
        assert "usuario" not in sess


def test_login_valido(monkeypatch, client):
    # Arrange
    user = UsuarioPrueba("usuario@ejemplo.com")
    verificar_mock = Mock(return_value=user)
    monkeypatch.setattr(
        "src.routes.vista_usuarios.verificar_credenciales",
        verificar_mock,
    )

    # Act
    resp = client.post(
        "/login",
        json={"correo": "usuario@ejemplo.com", "contrasena": "ValidPass1!"},
    )

    # Assert
    assert_that(resp.status_code, is_(equal_to(200)))
    data = resp.get_json()
    assert_that(data["success"], is_(equal_to(True)))
    assert_that(data["redirect"], is_(equal_to("/home")))
    assert_that(data["usuario"]["correo"], is_(equal_to("usuario@ejemplo.com")))
    verificar_mock.assert_called_once_with("usuario@ejemplo.com", "ValidPass1!")
    with client.session_transaction() as sess:
        assert_that(sess["usuario"]["correo"], is_(equal_to("usuario@ejemplo.com")))


def test_login_sin_body(client):
    resp = client.post("/login")

    # request.get_json() devuelve None -> 415 campos requeridos
    assert_that(resp.status_code, is_(equal_to(415)))


def test_login_contrasena_vacia(client):
    resp = client.post(
        "/login",
        json={"correo": "usuario@ejemplo.com", "contrasena": ""},
    )

    # Campo presente pero vacío -> llega al controlador y responde 401
    assert_that(resp.status_code, is_(equal_to(401)))
    data = resp.get_json()
    assert_that(data["error"], is_(equal_to("Credenciales inválidas")))


def test_login_valida_sesion_permanente(monkeypatch, client):
    """Cuando hacemos login exitoso la sesion debe marcarse permanente"""
    monkeypatch.setattr(
        "src.routes.vista_usuarios.verificar_credenciales",
        lambda correo, contrasena: UsuarioPrueba(correo),
    )

    resp = client.post(
        "/login",
        json={"correo": "usuario@ejemplo.com", "contrasena": "ValidPass1!"},
    )

    assert_that(resp.status_code, is_(equal_to(200)))
    with client.session_transaction() as sess:
        assert_that(sess.permanent, is_(equal_to(True)))


def test_login_dos_usuarios_contra_mismas_credenciales(monkeypatch, client):
    """Simula dos correos posibles y solo acepta el correcto."""

    def verificar_fake(correo, contrasena):
        if correo == "valido@ejemplo.com" and contrasena == "ClaveValida1!":
            return UsuarioPrueba(correo)
        if correo == "otro@ejemplo.com" and contrasena == "ClaveValida1!":
            # un usuario diferente, misma contraseña, se rechaza
            return None
        return None

    monkeypatch.setattr(
        "src.routes.vista_usuarios.verificar_credenciales",
        verificar_fake,
    )

    # Primer intento: correo incorrecto
    respuesta_mala = client.post(
        "/login",
        json={"correo": "otro@ejemplo.com", "contrasena": "ClaveValida1!"},
    )
    assert_that(respuesta_mala.status_code, is_(equal_to(401)))

    # Segundo intento: correo correcto
    respuesta_buena = client.post(
        "/login",
        json={"correo": "valido@ejemplo.com", "contrasena": "ClaveValida1!"},
    )
    assert_that(respuesta_buena.status_code, is_(equal_to(200)))
    with client.session_transaction() as sess:
        assert_that(sess["usuario"]["correo"], is_(equal_to("valido@ejemplo.com")))
