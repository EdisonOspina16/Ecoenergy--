import pytest
from psycopg2 import Error as DatabaseError
from src.domain.errors import PersistenciaError, ConexionError
from src.aplication.service import dispositivos_service as ds


# CONSTANTES DE PRUEBA
FILA_DISPOSITIVO_ENCENDIDO  = ("Televisor",  150.0, True,  "television")
FILA_DISPOSITIVO_APAGADO    = ("Lámpara",    0.0,   False, "lampara")
FILA_DISPOSITIVO_SIN_WATTS  = ("Ventilador", None,  True,  "ventilador")
FILA_DISPOSITIVO_SIN_NOMBRE = (None,         80.0,  True,  "aire_acondicionado")
FILA_DISPOSITIVO_COMPUTADOR = ("Computador", 300.0, False, "computador")

# ==============================================================
# INFRAESTRUCTURA DE PRUEBA (Objetos Fake y Helper Stub)
# ==============================================================

class DummyCursor:
    """
    Fake: Implementación funcional simplificada de un cursor de base de datos.
    Retorna filas configuradas por el test y lanza DatabaseError
    cuando se activa el flag error_bd.
    """

    def __init__(self, filas: list, error_bd: bool = False) -> None:
        self.filas = filas
        self.error_bd = error_bd
        self.closed: bool = False

    def execute(self, query: str, params: tuple = None) -> None:
        if self.error_bd:
            raise DatabaseError("connection lost")

    def fetchall(self) -> list:
        return self.filas

    def close(self) -> None:
        self.closed = True


class DummyConnection:
    """
    Fake: Implementación funcional simplificada de una conexión a BD.
    Retorna un DummyCursor con las filas configuradas por cada test.
    No interactúa con una base de datos real.
    """

    def __init__(self, filas: list, error_bd: bool = False) -> None:
        self.closed: bool = False
        self.filas = filas
        self.error_bd = error_bd

    def cursor(self, cursor_factory=None) -> DummyCursor:
        return DummyCursor(self.filas, self.error_bd)

    def close(self) -> None:
        self.closed = True


def make_fake_db(monkeypatch: pytest.MonkeyPatch, filas: list, error_bd: bool = False) -> DummyConnection:
    """
    Stub: reemplaza obtener_conexion() en el service con una DummyConnection
    configurada con las filas del test, forzando el flujo sin BD real.
    """
    conn = DummyConnection(filas, error_bd)
    monkeypatch.setattr(ds, "obtener_conexion", lambda: conn)
    return conn


# ==============================================================
# CP-MD-01: MOSTRAR ESTADO DESCONECTADO
# ==============================================================

def test_dispositivo_apagado_muestra_estado_apagado(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-MD-01: Un dispositivo con estado_activo=False debe mostrar estado 'Apagado'."""
    # Arrange — Stub: fuerza retorno de dispositivo apagado
    make_fake_db(monkeypatch, [FILA_DISPOSITIVO_APAGADO])

    # Act
    resultado = ds.obtener_dispositivos()

    # Assert
    assert len(resultado) == 1
    assert resultado[0]["estado"] == "Apagado"
    assert resultado[0]["nombre"] == "Lámpara"


# ==============================================================
# CP-MD-02: CAMBIAR ESTADO DE DESCONECTADO A CONECTADO
# ==============================================================

def test_dispositivo_cambia_a_encendido(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-MD-02: Al conectar un dispositivo su estado debe cambiar a 'Encendido'."""
    # Arrange — Dummy: simula dispositivo que fue conectado (estado_activo=True)
    dispositivo_conectado = ("Televisor", 150.0, True, "television")
    make_fake_db(monkeypatch, [dispositivo_conectado])  # Stub

    # Act
    resultado = ds.obtener_dispositivos()

    # Assert
    assert len(resultado) == 1
    assert resultado[0]["estado"] == "Encendido"


# ==============================================================
# CP-MD-03: MOSTRAR ESTADO CONECTADO
# ==============================================================

def test_dispositivo_encendido_muestra_estado_encendido(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-MD-03: Un dispositivo con estado_activo=True debe mostrar estado 'Encendido'."""
    # Arrange — Stub: fuerza retorno de dispositivo encendido
    make_fake_db(monkeypatch, [FILA_DISPOSITIVO_ENCENDIDO])

    # Act
    resultado = ds.obtener_dispositivos()

    # Assert
    assert len(resultado) == 1
    assert resultado[0]["estado"] == "Encendido"
    assert resultado[0]["nombre"] == "Televisor"
    assert resultado[0]["watts"] == pytest.approx(150.0)


# ==============================================================
# CP-MD-04: CAMBIAR ESTADO DE CONECTADO A DESCONECTADO
# ==============================================================

def test_dispositivo_cambia_a_apagado(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-MD-04: Al desconectar un dispositivo su estado debe cambiar a 'Apagado'."""
    # Arrange — Dummy: simula dispositivo que fue desconectado (estado_activo=False)
    dispositivo_desconectado = ("Televisor", 0.0, False, "television")
    make_fake_db(monkeypatch, [dispositivo_desconectado])  # Stub

    # Act
    resultado = ds.obtener_dispositivos()

    # Assert
    assert len(resultado) == 1
    assert resultado[0]["estado"] == "Apagado"


# ==============================================================
# CP-MD-05: MANTENER ESTADO DESPUÉS DE RECARGAR PÁGINA
# ==============================================================

def test_estado_se_mantiene_en_llamadas_consecutivas(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-MD-05: El estado de los dispositivos debe mantenerse igual en llamadas consecutivas."""
    # Arrange — Stub: fuerza el mismo retorno en dos llamadas consecutivas
    make_fake_db(monkeypatch, [FILA_DISPOSITIVO_ENCENDIDO, FILA_DISPOSITIVO_APAGADO])

    # Act
    resultado_1 = ds.obtener_dispositivos()
    make_fake_db(monkeypatch, [FILA_DISPOSITIVO_ENCENDIDO, FILA_DISPOSITIVO_APAGADO])
    resultado_2 = ds.obtener_dispositivos()

    # Assert
    assert len(resultado_1) == len(resultado_2)
    assert resultado_1[0]["estado"] == resultado_2[0]["estado"]
    assert resultado_1[1]["estado"] == resultado_2[1]["estado"]


# ==============================================================
# CP-MD-06: MOSTRAR ESTADOS CORRECTOS EN MÚLTIPLES DISPOSITIVOS
# ==============================================================

def test_multiples_dispositivos_muestran_estados_correctos(monkeypatch: pytest.MonkeyPatch) -> None:
    """CP-MD-06: Con múltiples dispositivos cada uno debe mostrar su estado correcto."""
    # Arrange — Stub: fuerza retorno de dos dispositivos con estados distintos
    make_fake_db(monkeypatch, [FILA_DISPOSITIVO_ENCENDIDO, FILA_DISPOSITIVO_COMPUTADOR])

    # Act
    resultado = ds.obtener_dispositivos()

    # Assert
    assert len(resultado) == 2
    assert resultado[0]["estado"] == "Encendido"
    assert resultado[0]["nombre"] == "Televisor"
    assert resultado[1]["estado"] == "Apagado"
    assert resultado[1]["nombre"] == "Computador"


# ==============================================================
# PRUEBA DE CONSUMO CALCULADO CORRECTAMENTE
# ==============================================================

def test_consumo_se_calcula_en_kwh(monkeypatch: pytest.MonkeyPatch) -> None:
    """El consumo debe convertirse de watts a kWh dividiendo entre 1000."""
    # Arrange — Stub: dispositivo con 150 watts
    make_fake_db(monkeypatch, [FILA_DISPOSITIVO_ENCENDIDO])

    # Act
    resultado = ds.obtener_dispositivos()

    # Assert
    assert resultado[0]["consumo"] == pytest.approx(0.15)  # 150 / 1000
    assert resultado[0]["watts"] == pytest.approx(150.0)


# ==============================================================
# PRUEBA DE DISPOSITIVO SIN WATTS REGISTRADOS
# ==============================================================

def test_dispositivo_sin_watts_retorna_consumo_cero(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un dispositivo sin registro de consumo debe retornar consumo=0.0 y watts=0.0."""
    # Arrange — Stub: dispositivo sin watts (None)
    make_fake_db(monkeypatch, [FILA_DISPOSITIVO_SIN_WATTS])

    # Act
    resultado = ds.obtener_dispositivos()

    # Assert
    assert resultado[0]["consumo"] == pytest.approx(0.0)
    assert resultado[0]["watts"] == pytest.approx(0.0)


# ==============================================================
# PRUEBA DE DISPOSITIVO SIN NOMBRE
# ==============================================================

def test_dispositivo_sin_nombre_usa_tipo_o_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Un dispositivo sin alias debe usar tipo_dispositivo_ia o 'Dispositivo Sin Nombre'."""
    # Arrange — Stub: dispositivo sin alias (None)
    make_fake_db(monkeypatch, [FILA_DISPOSITIVO_SIN_NOMBRE])

    # Act
    resultado = ds.obtener_dispositivos()

    # Assert
    assert resultado[0]["nombre"] in ["aire_acondicionado", "Dispositivo Sin Nombre"]


# ==============================================================
# PRUEBA SIN DISPOSITIVOS
# ==============================================================

def test_sin_dispositivos_retorna_lista_vacia(monkeypatch: pytest.MonkeyPatch) -> None:
    """Cuando no hay dispositivos registrados debe retornar lista vacía."""
    # Arrange — Stub: fuerza retorno de lista vacía
    make_fake_db(monkeypatch, [])

    # Act
    resultado = ds.obtener_dispositivos()

    # Assert
    assert resultado == []


# ==============================================================
# PRUEBA DE SIN CONEXIÓN A BASE DE DATOS
# ==============================================================

def test_sin_conexion_bd_lanza_conexion_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Stub: cuando obtener_conexion() retorna None debe lanzar ConexionError."""
    # Arrange — Stub: fuerza obtener_conexion() a retornar None
    monkeypatch.setattr(ds, "obtener_conexion", lambda: None)

    # Act & Assert
    with pytest.raises(ConexionError) as exc_info:
        ds.obtener_dispositivos()

    assert "no se pudo conectar" in str(exc_info.value).lower()


# ==============================================================
# PRUEBA DE ERROR GENÉRICO DE BASE DE DATOS
# ==============================================================

def test_error_generico_base_datos_lanza_persistencia_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Fake: el DummyCursor lanza DatabaseError cuando error_bd=True,
    lo que debe propagarse como PersistenciaError desde el repository.
    """
    # Arrange — Stub + Fake: conexión lista, cursor dispara error interno
    make_fake_db(monkeypatch, [], error_bd=True)

    # Act & Assert
    with pytest.raises(PersistenciaError) as exc_info:
        ds.obtener_dispositivos()

    assert "error en base de datos" in str(exc_info.value).lower()