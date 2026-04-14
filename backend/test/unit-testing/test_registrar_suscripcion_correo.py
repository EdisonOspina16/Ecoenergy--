import pytest
from psycopg2 import Error as DatabaseError
from src.domain.errors import ValidacionError, PersistenciaError, ConexionError, CorreoDuplicadoError
from src.aplication.service import subscriber_service as ss

# CONSTANTES DE PRUEBA

CORREO_VALIDO           = "prueba1@gmail.com"
CORREO_DUPLICADO        = "duplicado@gmail.com"
CORREO_ERROR_BD         = "error@gmail.com"
CORREO_ESPECIALES       = "prueba_1+tag@correo.co"
CORREO_SIN_ARROBA       = "usuariocorreo.com"
CORREO_SIN_DOMINIO      = "usuario@"
CORREO_SIN_EXTENSION    = "usuario@gmail"
CORREO_CON_ESPACIOS     = "usuario @gmail.com"


# ==============================================================
# INFRAESTRUCTURA DE PRUEBA (Objetos Fake y Helper Stub)
# ==============================================================

class DummyCursor:
    """
    Fake: Implementación funcional simplificada de un cursor de BD.
    Simula INSERT exitoso, duplicado o error genérico según el correo.
    """

    def __init__(self) -> None:
        self.closed: bool = False

    def execute(self, query: str, params: tuple) -> None:
        email = params[0]
        if email == CORREO_DUPLICADO:
            raise DatabaseError("duplicate key value violates unique constraint")
        if email == CORREO_ERROR_BD:
            raise DatabaseError("connection lost")

    def close(self) -> None:
        self.closed = True


class DummyConnection:
    """
    Fake: Implementación funcional simplificada de una conexión a BD.
    Registra commit, rollback y cierre sin interactuar con una BD real.
    """

    def __init__(self) -> None:
        self.committed: bool = False
        self.closed: bool = False
        self.rolled_back: bool = False

    def cursor(self, cursor_factory=None) -> DummyCursor:
        return DummyCursor()

    def commit(self) -> None:
        self.committed = True

    def close(self) -> None:
        self.closed = True

    def rollback(self) -> None:
        self.rolled_back = True


@pytest.fixture(autouse=True)
def fake_db(monkeypatch: pytest.MonkeyPatch) -> DummyConnection:
    """
    Fixture compartido (Arrange global):
    - Stub: reemplaza obtener_conexion() con DummyConnection.
    - Stub: reemplaza send_welcome_email() con versión sin efecto.
    Se aplica automáticamente a todas las pruebas del módulo.
    """
    conn = DummyConnection()
    monkeypatch.setattr(ss, "obtener_conexion", lambda: conn)
    monkeypatch.setattr(ss, "send_welcome_email", lambda email: None)
    return conn


# ==============================================================
# CP-SC-01: REGISTRO EXITOSO CON CORREO VÁLIDO
# ==============================================================

def test_correo_valido_registra_exitosamente(fake_db: DummyConnection) -> None:
    """CP-SC-01: Un correo válido debe registrarse exitosamente."""
    # Arrange
    email = CORREO_VALIDO

    # Act
    exito, mensaje = ss.subscribe_user(email)

    # Assert
    assert exito is True
    assert "registrado" in mensaje.lower()


def test_correo_valido_hace_commit(fake_db: DummyConnection) -> None:
    """CP-SC-01: Tras registrar exitosamente debe realizarse commit en la BD."""
    # Arrange
    email = CORREO_VALIDO

    # Act
    ss.subscribe_user(email)

    # Assert — Spy: commit se ejecutó
    assert fake_db.committed is True


def test_correo_valido_envia_bienvenida(monkeypatch: pytest.MonkeyPatch, fake_db: DummyConnection) -> None:
    """CP-SC-01: Tras registrar exitosamente debe enviarse el correo de bienvenida."""
    # Arrange
    email = CORREO_VALIDO
    emails_enviados = []

    # Spy: registra los correos enviados
    monkeypatch.setattr(ss, "send_welcome_email", lambda e: emails_enviados.append(e))

    # Act
    ss.subscribe_user(email)

    # Assert — Spy: se envió el correo de bienvenida
    assert email in emails_enviados


# ==============================================================
# CP-SC-02: CORREO CON FORMATO INVÁLIDO
# ==============================================================

def test_correo_sin_arroba_lanza_validacion_error(fake_db: DummyConnection) -> None:
    """CP-SC-02: Un correo sin @ debe lanzar ValidacionError."""
    # Arrange
    email = CORREO_SIN_ARROBA

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        ss.subscribe_user(email)

    assert "correo inválido" in str(exc_info.value).lower()


def test_correo_sin_dominio_lanza_validacion_error(fake_db: DummyConnection) -> None:
    """CP-SC-02: Un correo sin dominio después del @ debe lanzar ValidacionError."""
    # Arrange
    email = CORREO_SIN_DOMINIO

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        ss.subscribe_user(email)

    assert "correo inválido" in str(exc_info.value).lower()


def test_correo_sin_extension_lanza_validacion_error(fake_db: DummyConnection) -> None:
    """CP-SC-02: Un correo sin extensión (.com, .co) debe lanzar ValidacionError."""
    # Arrange
    email = CORREO_SIN_EXTENSION

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        ss.subscribe_user(email)

    assert "correo inválido" in str(exc_info.value).lower()


def test_correo_con_espacios_lanza_validacion_error(fake_db: DummyConnection) -> None:
    """CP-SC-02: Un correo con espacios debe lanzar ValidacionError."""
    # Arrange
    email = CORREO_CON_ESPACIOS

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        ss.subscribe_user(email)

    assert "correo inválido" in str(exc_info.value).lower()


# ==============================================================
# CP-SC-03: CORREO YA REGISTRADO (DUPLICADO)
# ==============================================================

def test_correo_duplicado_retorna_false(fake_db: DummyConnection) -> None:
    """CP-SC-03: Un correo ya registrado debe retornar (False, 'Correo ya registrado')."""
    # Arrange
    email = CORREO_DUPLICADO

    # Act
    exito, mensaje = ss.subscribe_user(email)

    # Assert
    assert exito is False
    assert "ya registrado" in mensaje.lower()


def test_correo_duplicado_no_envia_bienvenida(monkeypatch: pytest.MonkeyPatch, fake_db: DummyConnection) -> None:
    """CP-SC-03: Si el correo ya existe no debe enviarse el correo de bienvenida."""
    # Arrange
    email = CORREO_DUPLICADO
    emails_enviados = []

    # Spy: registra si se intentó enviar
    monkeypatch.setattr(ss, "send_welcome_email", lambda e: emails_enviados.append(e))

    # Act
    ss.subscribe_user(email)

    # Assert — Spy: no se envió correo de bienvenida
    assert len(emails_enviados) == 0


# ==============================================================
# CP-SC-04: CAMPO CORREO VACÍO
# ==============================================================

def test_correo_vacio_lanza_validacion_error(fake_db: DummyConnection) -> None:
    """CP-SC-04: Un correo vacío debe lanzar ValidacionError."""
    # Arrange
    email = ""

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        ss.subscribe_user(email)

    assert "correo obligatorio" in str(exc_info.value).lower()


def test_correo_nulo_lanza_validacion_error(fake_db: DummyConnection) -> None:
    """CP-SC-04: Un correo None debe lanzar ValidacionError."""
    # Arrange
    email = None

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        ss.subscribe_user(email)

    assert "correo obligatorio" in str(exc_info.value).lower()


# ==============================================================
# CP-SC-05: CORREO CON CARACTERES ESPECIALES VÁLIDOS
# ==============================================================

def test_correo_con_caracteres_especiales_validos(fake_db: DummyConnection) -> None:
    """CP-SC-05: Un correo con + y tag debe ser aceptado y registrado exitosamente."""
    # Arrange
    email = CORREO_ESPECIALES

    # Act
    exito, mensaje = ss.subscribe_user(email)

    # Assert
    assert exito is True
    assert "registrado" in mensaje.lower()


# ==============================================================
# PRUEBA DE SIN CONEXIÓN A BASE DE DATOS
# ==============================================================

def test_sin_conexion_bd_lanza_conexion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Stub: cuando obtener_conexion() retorna None debe lanzar ConexionError."""
    # Arrange — Stub: fuerza obtener_conexion() a retornar None
    monkeypatch.setattr(ss, "obtener_conexion", lambda: None)
    monkeypatch.setattr(ss, "send_welcome_email", lambda email: None)
    email = CORREO_VALIDO

    # Act & Assert
    with pytest.raises(ConexionError) as exc_info:
        ss.subscribe_user(email)

    assert "no se pudo conectar" in str(exc_info.value).lower()


# ==============================================================
# PRUEBA DE ERROR GENÉRICO DE BASE DE DATOS
# ==============================================================

def test_error_generico_base_datos_lanza_persistencia_error(fake_db: DummyConnection) -> None:
    """
    Fake: el DummyCursor lanza DatabaseError genérico para CORREO_ERROR_BD,
    lo que debe propagarse como PersistenciaError desde el repository.
    """
    # Arrange — Fake: cursor dispara error genérico de BD
    email = CORREO_ERROR_BD

    # Act & Assert
    with pytest.raises(PersistenciaError) as exc_info:
        ss.subscribe_user(email)

    assert "error en base de datos" in str(exc_info.value).lower()