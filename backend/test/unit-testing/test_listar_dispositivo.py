import pytest
from datetime import datetime
from psycopg2 import Error as DatabaseError
from src.domain.errors import ValidacionError, PersistenciaError, ConexionError
from src.aplication.service import dispositivos_service as ds

# ==============================================================
# CONSTANTES DE PRUEBA
# ==============================================================

ID_USUARIO_VALIDO   = 1
ID_USUARIO_INVALIDO = -1
ID_USUARIO_CERO     = 0
ID_USUARIO_ERROR_BD = 999

FECHA_CONEXION = datetime(2025, 1, 1, 10, 0, 0)

# Filas crudas que simula retornar RealDictCursor (diccionarios)
DISPOSITIVO_ACTIVO = {
    "id_dispositivos": 1,
    "id_hogar": 10,
    "alias": "Televisor",
    "id_dispositivo_iot": "iot-001",
    "tipo_dispositivo_ia": "television",
    "estado_activo": True,
    "fecha_conexion": FECHA_CONEXION,
}

DISPOSITIVO_INACTIVO = {
    "id_dispositivos": 2,
    "id_hogar": 10,
    "alias": "Lámpara",
    "id_dispositivo_iot": "iot-002",
    "tipo_dispositivo_ia": "lampara",
    "estado_activo": False,
    "fecha_conexion": FECHA_CONEXION,
}

DISPOSITIVO_VENTILADOR = {
    "id_dispositivos": 3,
    "id_hogar": 10,
    "alias": "Ventilador",
    "id_dispositivo_iot": "iot-003",
    "tipo_dispositivo_ia": "ventilador",
    "estado_activo": True,
    "fecha_conexion": FECHA_CONEXION,
}

DISPOSITIVO_COMPUTADOR = {
    "id_dispositivos": 4,
    "id_hogar": 10,
    "alias": "Computador",
    "id_dispositivo_iot": "iot-004",
    "tipo_dispositivo_ia": "computador",
    "estado_activo": True,
    "fecha_conexion": FECHA_CONEXION,
}

DISPOSITIVO_LAMPARA = {
    "id_dispositivos": 5,
    "id_hogar": 10,
    "alias": "Lámpara 2",
    "id_dispositivo_iot": "iot-005",
    "tipo_dispositivo_ia": "lampara",
    "estado_activo": True,
    "fecha_conexion": FECHA_CONEXION,
}


# ==============================================================
# INFRAESTRUCTURA DE PRUEBA (Objetos Dummy y Fixture)
# ==============================================================

class DummyCursor:
    """
    Fake: Simula un cursor RealDictCursor con comportamiento funcional
    simplificado. Retorna filas configuradas y lanza DatabaseError
    para id_usuario especial.
    """

    def __init__(self, filas: list) -> None:
        self.filas = filas
        self.closed: bool = False

    def execute(self, query: str, params: tuple) -> None:
        id_usuario = params[0]
        if id_usuario == ID_USUARIO_ERROR_BD:
            raise DatabaseError("connection lost")

    def fetchall(self) -> list:
        return self.filas

    def close(self) -> None:
        self.closed = True


class DummyConnection:
    """
    Fake: Simula una conexión a base de datos con cursor configurable
    según el escenario de prueba.
    """

    def __init__(self, filas: list) -> None:
        self.closed: bool = False
        self.filas = filas

    def cursor(self, cursor_factory=None) -> DummyCursor:
        return DummyCursor(self.filas)

    def close(self) -> None:
        self.closed = True


def make_fake_db(monkeypatch, filas: list) -> DummyConnection:
    """
    Helper — Stub: crea un DummyConnection con las filas dadas y
    reemplaza obtener_conexion() en el service con una respuesta controlada.
    """
    conn = DummyConnection(filas)
    monkeypatch.setattr(ds, "obtener_conexion", lambda: conn)
    return conn


# ==============================================================
# CP-LD-01: DISPOSITIVO ACTIVO
# ==============================================================

def test_dispositivo_activo_retorna_estado_activo(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-LD-01: Un dispositivo activo debe aparecer en la lista con estado_activo=True."""
    # Arrange
    make_fake_db(monkeypatch, [DISPOSITIVO_ACTIVO])
    id_usuario = ID_USUARIO_VALIDO

    # Act
    resultado = ds.listar_dispositivos(id_usuario)

    # Assert
    assert len(resultado) == 1
    assert resultado[0].estado_activo is True
    assert resultado[0].alias == "Televisor"


# ==============================================================
# CP-LD-02: DISPOSITIVO INACTIVO
# ==============================================================

def test_dispositivo_inactivo_retorna_estado_inactivo(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-LD-02: Un dispositivo inactivo debe aparecer en la lista con estado_activo=False."""
    # Arrange
    make_fake_db(monkeypatch, [DISPOSITIVO_INACTIVO])
    id_usuario = ID_USUARIO_VALIDO

    # Act
    resultado = ds.listar_dispositivos(id_usuario)

    # Assert
    assert len(resultado) == 1
    assert resultado[0].estado_activo is False
    assert resultado[0].alias == "Lámpara"


# ==============================================================
# CP-LD-03: CONSUMO INDIVIDUAL DIFERENTE POR DISPOSITIVO
# ==============================================================

def test_multiples_dispositivos_retorna_todos(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-LD-03: Con múltiples dispositivos, cada uno debe aparecer individualmente."""
    # Arrange
    filas = [DISPOSITIVO_ACTIVO, DISPOSITIVO_COMPUTADOR, DISPOSITIVO_LAMPARA]
    make_fake_db(monkeypatch, filas)
    id_usuario = ID_USUARIO_VALIDO

    # Act
    resultado = ds.listar_dispositivos(id_usuario)

    # Assert
    assert len(resultado) == 3
    aliases = [d.alias for d in resultado]
    assert "Televisor" in aliases
    assert "Computador" in aliases
    assert "Lámpara 2" in aliases


# ==============================================================
# CP-LD-04: SIN DISPOSITIVOS REGISTRADOS
# ==============================================================

def test_sin_dispositivos_retorna_lista_vacia(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-LD-04: Un usuario sin dispositivos debe retornar lista vacía."""
    # Arrange
    make_fake_db(monkeypatch, [])
    id_usuario = ID_USUARIO_VALIDO

    # Act
    resultado = ds.listar_dispositivos(id_usuario)

    # Assert
    assert resultado == []
    assert len(resultado) == 0


# ==============================================================
# CP-LD-05: UN SOLO DISPOSITIVO REGISTRADO
# ==============================================================

def test_un_solo_dispositivo_retorna_lista_con_uno(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-LD-05: Un usuario con un solo dispositivo debe retornar lista con un elemento."""
    # Arrange
    make_fake_db(monkeypatch, [DISPOSITIVO_ACTIVO])
    id_usuario = ID_USUARIO_VALIDO

    # Act
    resultado = ds.listar_dispositivos(id_usuario)

    # Assert
    assert len(resultado) == 1
    assert resultado[0].alias == "Televisor"


# ==============================================================
# CP-LD-17: REFRESCAR PÁGINA MANTIENE DATOS
# ==============================================================

def test_llamadas_consecutivas_retornan_mismos_datos(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-LD-17: Llamadas consecutivas deben retornar los mismos dispositivos."""
    # Arrange
    make_fake_db(monkeypatch, [DISPOSITIVO_ACTIVO, DISPOSITIVO_INACTIVO])
    id_usuario = ID_USUARIO_VALIDO

    # Act
    resultado_1 = ds.listar_dispositivos(id_usuario)
    make_fake_db(monkeypatch, [DISPOSITIVO_ACTIVO, DISPOSITIVO_INACTIVO])
    resultado_2 = ds.listar_dispositivos(id_usuario)

    # Assert
    assert len(resultado_1) == len(resultado_2)
    assert resultado_1[0].alias == resultado_2[0].alias
    assert resultado_1[1].alias == resultado_2[1].alias


# ==============================================================
# CP-LD-07: DISPOSITIVO CONECTADO (estado_activo=True)
# ==============================================================

def test_dispositivo_conectado_aparece_como_activo(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-LD-07: Al conectar un dispositivo debe aparecer con estado_activo=True."""
    # Arrange
    dispositivo_conectado = {**DISPOSITIVO_VENTILADOR, "estado_activo": True}
    make_fake_db(monkeypatch, [dispositivo_conectado])
    id_usuario = ID_USUARIO_VALIDO

    # Act
    resultado = ds.listar_dispositivos(id_usuario)

    # Assert
    assert len(resultado) == 1
    assert resultado[0].estado_activo is True
    assert resultado[0].alias == "Ventilador"


# ==============================================================
# CP-LD-08: DISPOSITIVO DESCONECTADO (estado_activo=False)
# ==============================================================

def test_dispositivo_desconectado_aparece_como_inactivo(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-LD-08: Al desconectar un dispositivo debe aparecer con estado_activo=False."""
    # Arrange
    dispositivo_desconectado = {**DISPOSITIVO_VENTILADOR, "estado_activo": False}
    make_fake_db(monkeypatch, [dispositivo_desconectado])
    id_usuario = ID_USUARIO_VALIDO

    # Act
    resultado = ds.listar_dispositivos(id_usuario)

    # Assert
    assert len(resultado) == 1
    assert resultado[0].estado_activo is False


# ==============================================================
# PRUEBAS DE VALIDACIÓN DE ID_USUARIO
# ==============================================================

def test_id_usuario_negativo_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un id_usuario negativo debe lanzar ValidacionError antes de consultar la BD."""
    # Arrange
    make_fake_db(monkeypatch, [])
    id_usuario = ID_USUARIO_INVALIDO

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        ds.listar_dispositivos(id_usuario)

    assert "id de usuario inválido" in str(exc_info.value).lower()


def test_id_usuario_cero_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un id_usuario igual a 0 debe lanzar ValidacionError."""
    # Arrange
    make_fake_db(monkeypatch, [])
    id_usuario = ID_USUARIO_CERO

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        ds.listar_dispositivos(id_usuario)

    assert "id de usuario inválido" in str(exc_info.value).lower()


def test_id_usuario_nulo_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un id_usuario None debe lanzar ValidacionError."""
    # Arrange
    make_fake_db(monkeypatch, [])
    id_usuario = None

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        ds.listar_dispositivos(id_usuario)

    assert "id de usuario inválido" in str(exc_info.value).lower()


def test_id_usuario_string_lanza_validacion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un id_usuario de tipo string debe lanzar ValidacionError."""
    # Arrange
    make_fake_db(monkeypatch, [])
    id_usuario = "abc"

    # Act & Assert
    with pytest.raises(ValidacionError) as exc_info:
        ds.listar_dispositivos(id_usuario)

    assert "id de usuario inválido" in str(exc_info.value).lower()


# ==============================================================
# PRUEBA DE SIN CONEXIÓN A BASE DE DATOS
# ==============================================================

def test_sin_conexion_bd_lanza_conexion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Stub: cuando obtener_conexion() retorna None debe lanzar ConexionError."""
    # Arrange
    monkeypatch.setattr(ds, "obtener_conexion", lambda: None)
    id_usuario = ID_USUARIO_VALIDO

    # Act & Assert
    with pytest.raises(ConexionError) as exc_info:
        ds.listar_dispositivos(id_usuario)

    assert "no se pudo conectar" in str(exc_info.value).lower()


# ==============================================================
# PRUEBA DE ERROR GENÉRICO DE BASE DE DATOS
# ==============================================================

def test_error_generico_base_datos_lanza_persistencia_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un error inesperado de BD debe lanzar PersistenciaError."""
    # Arrange
    make_fake_db(monkeypatch, [])
    id_usuario = ID_USUARIO_ERROR_BD  # dispara DatabaseError en el DummyCursor

    # Act & Assert
    with pytest.raises(PersistenciaError) as exc_info:
        ds.listar_dispositivos(id_usuario)

    assert "error en base de datos" in str(exc_info.value).lower()