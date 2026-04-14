import pytest
from psycopg2 import Error as DatabaseError
from src.domain.errors import ValidacionError, PersistenciaError, ConexionError
from src.aplication.service import hogar_service as hs

# ==============================================================
# CONSTANTES DE PRUEBA
# Dummy: datos de relleno que simulan parámetros y filas de BD.
# ==============================================================

ID_USUARIO_VALIDO   = 1
ID_USUARIO_INVALIDO = -1
ID_USUARIO_CERO     = 0

NOMBRE_HOGAR_VALIDO  = "Mi casa"
DIRECCION_VALIDA     = "Calle 72#46D-33, Sabaneta"

FILA_HOGAR_CREADO = {
    "id_hogar": 10,
    "id_usuario": ID_USUARIO_VALIDO,
    "direccion": DIRECCION_VALIDA,
    "nombre_hogar": NOMBRE_HOGAR_VALIDO,
}


# ==============================================================
# INFRAESTRUCTURA DE PRUEBA (Objetos Fake y Helper Stub)
# ==============================================================

class DummyCursor:
    """
    Fake: Implementación funcional simplificada de un cursor RealDictCursor.
    Retorna la fila configurada por el test y registra commit/close.
    """

    def __init__(self, fila: dict | None, error_bd: bool = False) -> None:
        self.fila = fila
        self.error_bd = error_bd
        self.closed: bool = False

    def execute(self, query: str, params: tuple) -> None:
        if self.error_bd:
            raise DatabaseError("connection lost")

    def fetchone(self) -> dict | None:
        return self.fila

    def close(self) -> None:
        self.closed = True


class DummyConnection:
    """
    Fake: Implementación funcional simplificada de una conexión a BD.
    Registra commit, rollback y cierre sin interactuar con una BD real.
    """

    def __init__(self, fila: dict | None, error_bd: bool = False) -> None:
        self.committed: bool = False
        self.closed: bool = False
        self.rolled_back: bool = False
        self.fila = fila
        self.error_bd = error_bd

    def cursor(self, cursor_factory=None) -> DummyCursor:
        return DummyCursor(self.fila, self.error_bd)

    def commit(self) -> None:
        self.committed = True

    def close(self) -> None:
        self.closed = True

    def rollback(self) -> None:
        self.rolled_back = True


def make_fake_db(monkeypatch: pytest.MonkeyPatch, fila: dict | None, error_bd: bool = False) -> DummyConnection:
    """
    Stub: reemplaza obtener_conexion() en el service con una DummyConnection
    configurada con la fila del test, forzando el flujo sin BD real.
    """
    conn = DummyConnection(fila, error_bd)
    monkeypatch.setattr(hs, "obtener_conexion", lambda: conn)
    return conn


# ==============================================================
# CP-CH-01: CREAR PERFIL HOGAR EXITOSAMENTE
# ==============================================================

def test_crear_hogar_exitoso(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-CH-01: Con datos válidos debe crear el hogar y retornar objeto Hogar."""
    # Arrange — Stub: fuerza retorno de fila creada exitosamente
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)

    # Act
    resultado = hs.crear_hogar(ID_USUARIO_VALIDO, DIRECCION_VALIDA, NOMBRE_HOGAR_VALIDO)

    # Assert
    assert resultado is not None
    assert resultado.nombre_hogar == NOMBRE_HOGAR_VALIDO
    assert resultado.direccion == DIRECCION_VALIDA
    assert resultado.id_usuario == ID_USUARIO_VALIDO


def test_crear_hogar_hace_commit(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-CH-01: Tras crear el hogar exitosamente debe realizarse commit en la BD."""
    # Arrange — Spy: verificamos que se hizo commit
    fake_db = make_fake_db(monkeypatch, FILA_HOGAR_CREADO)

    # Act
    hs.crear_hogar(ID_USUARIO_VALIDO, DIRECCION_VALIDA, NOMBRE_HOGAR_VALIDO)

    # Assert — Spy: commit se ejecutó
    assert fake_db.committed is True


# ==============================================================
# CP-CH-02: NOMBRE VACÍO
# ==============================================================

def test_nombre_hogar_vacio_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-CH-02: Un nombre de hogar vacío debe lanzar ValidacionError."""
    # Arrange — Stub: conexión lista pero validación debe fallar antes
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        hs.crear_hogar(ID_USUARIO_VALIDO, DIRECCION_VALIDA, "")

    assert "nombre del hogar inválido" in str(exc_info.value).lower()


def test_nombre_hogar_nulo_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un nombre de hogar None debe lanzar ValidacionError."""
    # Arrange
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        hs.crear_hogar(ID_USUARIO_VALIDO, DIRECCION_VALIDA, None)

    assert "nombre del hogar inválido" in str(exc_info.value).lower()


def test_nombre_hogar_un_caracter_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un nombre de hogar de 1 carácter está bajo el mínimo y debe ser rechazado."""
    # Arrange
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        hs.crear_hogar(ID_USUARIO_VALIDO, DIRECCION_VALIDA, "A")

    assert "nombre del hogar inválido" in str(exc_info.value).lower()


def test_nombre_hogar_mayor_50_caracteres_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un nombre de hogar mayor a 50 caracteres debe ser rechazado."""
    # Arrange
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)
    nombre_largo = "A" * 51

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        hs.crear_hogar(ID_USUARIO_VALIDO, DIRECCION_VALIDA, nombre_largo)

    assert "nombre del hogar inválido" in str(exc_info.value).lower()


# ==============================================================
# CP-CH-03: DIRECCIÓN VACÍA
# ==============================================================

def test_direccion_vacia_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-CH-03: Una dirección vacía debe lanzar ValidacionError."""
    # Arrange — Stub: conexión lista pero validación debe fallar antes
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        hs.crear_hogar(ID_USUARIO_VALIDO, "", NOMBRE_HOGAR_VALIDO)

    assert "dirección inválida" in str(exc_info.value).lower()


def test_direccion_nula_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Una dirección None debe lanzar ValidacionError."""
    # Arrange
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        hs.crear_hogar(ID_USUARIO_VALIDO, None, NOMBRE_HOGAR_VALIDO)

    assert "dirección inválida" in str(exc_info.value).lower()


def test_direccion_mayor_100_caracteres_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Una dirección mayor a 100 caracteres debe ser rechazada."""
    # Arrange
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)
    direccion_larga = "Calle " + "A" * 96

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        hs.crear_hogar(ID_USUARIO_VALIDO, direccion_larga, NOMBRE_HOGAR_VALIDO)

    assert "dirección inválida" in str(exc_info.value).lower()


# ==============================================================
# CP-CH-04: NOMBRE CON CARACTERES ESPECIALES
# ==============================================================

def test_nombre_hogar_con_asterisco_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-CH-04: Un nombre con * debe lanzar ValidacionError."""
    # Arrange
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        hs.crear_hogar(ID_USUARIO_VALIDO, DIRECCION_VALIDA, "Mi **")

    assert "nombre del hogar inválido" in str(exc_info.value).lower()


def test_nombre_hogar_con_arroba_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un nombre con @ debe lanzar ValidacionError."""
    # Arrange
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        hs.crear_hogar(ID_USUARIO_VALIDO, DIRECCION_VALIDA, "Casa@hogar")

    assert "nombre del hogar inválido" in str(exc_info.value).lower()


def test_nombre_hogar_con_signo_numeral_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un nombre con # debe lanzar ValidacionError."""
    # Arrange
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        hs.crear_hogar(ID_USUARIO_VALIDO, DIRECCION_VALIDA, "Casa #1")

    assert "nombre del hogar inválido" in str(exc_info.value).lower()


# ==============================================================
# CP-CH-05: ERROR DE CONEXIÓN AL GUARDAR
# ==============================================================

def test_sin_conexion_bd_lanza_conexion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-CH-05: Cuando obtener_conexion() retorna None debe lanzar ConexionError."""
    # Arrange — Stub: fuerza obtener_conexion() a retornar None
    monkeypatch.setattr(hs, "obtener_conexion", lambda: None)

    # Act & Assert
    with pytest.raises(ConexionError) as exc_info:
        hs.crear_hogar(ID_USUARIO_VALIDO, DIRECCION_VALIDA, NOMBRE_HOGAR_VALIDO)

    assert "no se pudo conectar" in str(exc_info.value).lower()


# ==============================================================
# PRUEBAS DE VALIDACIÓN DE ID_USUARIO
# ==============================================================

def test_id_usuario_negativo_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un id_usuario negativo debe lanzar ValidacionError antes de consultar la BD."""
    # Arrange — Stub: conexión lista pero validación debe fallar antes
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        hs.crear_hogar(ID_USUARIO_INVALIDO, DIRECCION_VALIDA, NOMBRE_HOGAR_VALIDO)

    assert "id de usuario inválido" in str(exc_info.value).lower()


def test_id_usuario_cero_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un id_usuario igual a 0 debe lanzar ValidacionError."""
    # Arrange
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        hs.crear_hogar(ID_USUARIO_CERO, DIRECCION_VALIDA, NOMBRE_HOGAR_VALIDO)

    assert "id de usuario inválido" in str(exc_info.value).lower()


def test_id_usuario_nulo_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un id_usuario None debe lanzar ValidacionError."""
    # Arrange
    make_fake_db(monkeypatch, FILA_HOGAR_CREADO)

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        hs.crear_hogar(None, DIRECCION_VALIDA, NOMBRE_HOGAR_VALIDO)

    assert "id de usuario inválido" in str(exc_info.value).lower()


# ==============================================================
# PRUEBA DE HOGAR NO CREADO (fila None)
# ==============================================================

def test_hogar_no_creado_retorna_none(monkeypatch: pytest.MonkeyPatch) -> None:
    """Si el INSERT no retorna fila, el service debe retornar None."""
    # Arrange — Stub: fuerza retorno de None (sin fila insertada)
    make_fake_db(monkeypatch, None)

    # Act
    resultado = hs.crear_hogar(ID_USUARIO_VALIDO, DIRECCION_VALIDA, NOMBRE_HOGAR_VALIDO)

    # Assert
    assert resultado is None


# ==============================================================
# PRUEBA DE ERROR GENÉRICO DE BASE DE DATOS
# ==============================================================

def test_error_generico_base_datos_lanza_persistencia_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Fake: el DummyCursor lanza DatabaseError cuando error_bd=True,
    lo que debe propagarse como PersistenciaError desde el repository.
    """
    # Arrange — Stub + Fake: conexión lista, cursor dispara error interno
    make_fake_db(monkeypatch, None, error_bd=True)

    # Act & Assert
    with pytest.raises(PersistenciaError) as exc_info:
        hs.crear_hogar(ID_USUARIO_VALIDO, DIRECCION_VALIDA, NOMBRE_HOGAR_VALIDO)

    assert "error en base de datos" in str(exc_info.value).lower()