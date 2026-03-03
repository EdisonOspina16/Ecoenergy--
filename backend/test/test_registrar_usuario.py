import os
import sys
from typing import Any
import pytest
from src.controller import controladorUsuarios as cu


class DummyCursor:
    """
    Cursor falso para evitar acceso real a la base de datos.
    Simula un INSERT y puede lanzar excepciones según los parámetros.
    """

    def __init__(self) -> None:
        self.last_query: str | None = None
        self.last_params: tuple[Any, ...] | None = None

    def execute(self, query: str, params: tuple[Any, ...]) -> None:
        self.last_query = query
        self.last_params = params

        # Desempaquetar parámetros esperados: (nombre, apellidos, correo, contraseña_hash)
        _, _, correo, _ = params

        # correo duplicado -> simulamos error de unicidad en BD
        if correo == "duplicado@gmail.com":
            raise Exception("duplicate key value violates unique constraint usuarios_correo_key")

    def close(self) -> None:
        pass


class DummyConnection:
    """
    Conexión falsa que entrega un DummyCursor y registra commit/cierre.
    """

    def __init__(self) -> None:
        self.committed = False
        self.closed = False
        self.cursor_obj = DummyCursor()

    def cursor(self) -> DummyCursor:
        return self.cursor_obj

    def commit(self) -> None:
        self.committed = True

    def close(self) -> None:
        self.closed = True


@pytest.fixture(autouse=True)
def fake_db(monkeypatch: pytest.MonkeyPatch) -> DummyConnection:
    """
    Parchea obtener_conexion y generate_password_hash para que las pruebas
    de registrar_usuario no dependan de una base de datos real.
    """

    conn = DummyConnection()

    monkeypatch.setattr(cu, "obtener_conexion", lambda: conn)
    monkeypatch.setattr(cu, "generate_password_hash", lambda pwd: f"hashed-{pwd}")

    return conn


# ------------------------------
# Casos de prueba para NOMBRE
# ------------------------------

@pytest.mark.parametrize(
    "nombre, esperado, caso",
    [
        ("Carlos", True, "CP-001 Nombre válido simple"),
        ("", False, "CP-002 Nombre vacío"),
        ("Car1os", False, "CP-003 Números en nombre"),
        ("Al", True, "CP-004 Nombre 2 caracteres (mínimo válido)"),
        ("A" * 51, False, "CP-005 Nombre 51 caracteres (excede máximo)"),
    ],
)
def test_registrar_usuario_nombre(nombre: str, esperado: bool, caso: str) -> None:
    resultado = cu.registrar_usuario(
        nombre=nombre,
        apellidos="Gómez",
        correo="usuario@gmail.com",
        contraseña="Abc123!@",
    )
    assert resultado is esperado, caso


# ------------------------------
# Casos de prueba para APELLIDO
# ------------------------------

@pytest.mark.parametrize(
    "apellidos, esperado, caso",
    [
        ("Gómez", True, "CP-006 Apellido simple válido"),
        ("García-López", True, "CP-007 Apellido con guion"),
        ("", False, "CP-008 Apellido vacío"),
        ("Go", True, "CP-009 Apellido 2 caracteres (mínimo válido)"),
        (None, False, "CP-010 Apellido nulo"),
    ],
)
def test_registrar_usuario_apellidos(apellidos: Any, esperado: bool, caso: str) -> None:
    resultado = cu.registrar_usuario(
        nombre="Carlos",
        apellidos=apellidos,
        correo="usuario@gmail.com",
        contraseña="Abc123!@",
    )
    assert resultado is esperado, caso


# ------------------------------
# Casos de prueba para CORREO
# ------------------------------

@pytest.mark.parametrize(
    "correo, esperado, caso",
    [
        ("usuario@gmail.com", True, "CP-011 Correo válido estándar"),
        ("usuariogmail.com", False, "CP-012 Correo sin @"),
        ("duplicado@gmail.com", False, "CP-013 Correo duplicado"),
        ("", False, "CP-014 Correo vacío"),
        ("u" * 245 + "@gmail.com", False, "CP-015 Correo >254 caracteres"),
        ("usuario@", False, "CP-016 Correo sin dominio"),
        ("usuario@gmail", False, "CP-017 Correo sin extensión"),
        ("user@@gmail.com", False, "CP-018 Correo doble @"),
        ("user @gmail.com", False, "CP-019 Correo con espacios"),
        ("Usuario@Gmail.COM", True, "CP-020 Correo mayúsculas"),
    ],
)
def test_registrar_usuario_correo(correo: str, esperado: bool, caso: str) -> None:
    resultado = cu.registrar_usuario(
        nombre="Carlos",
        apellidos="Gómez",
        correo=correo,
        contraseña="Abc123!@",
    )
    assert resultado is esperado, caso


# ------------------------------
# Casos de prueba para CONTRASEÑA
# ------------------------------

@pytest.mark.parametrize(
    "contraseña, esperado, caso",
    [
        ("Abc123!@", True, "CP-016 Contraseña válida fuerte"),
        ("abcdefgh", False, "CP-017 Solo minúsculas"),
        ("12345678", False, "CP-018 Solo números"),
        ("ABCDEFGH", False, "CP-019 Solo mayúsculas"),
        ("", False, "CP-020 Contraseña vacía"),
        (None, False, "CP-021 Contraseña nula"),
        ("Abc1!", False, "CP-022 Menos de 8 caracteres"),
        ("Abc123!@", True, "CP-023 Exactamente 8 caracteres"),
        ("Abc 123!", False, "CP-024 Con espacios en contraseña"),
        ("P@ssw0rd#", True, "CP-025 Caracteres especiales válidos"),
        ("A" * 130, False, "CP-026 Contraseña >128 caracteres"),
        ("Abc123😀", False, "CP-027 Contraseña con emoji"),
    ],
)
def test_registrar_usuario_contraseña(contraseña: Any, esperado: bool, caso: str) -> None:
    resultado = cu.registrar_usuario(
        nombre="Carlos",
        apellidos="Gómez",
        correo="usuario@gmail.com",
        contraseña=contraseña,
    )
    assert resultado is esperado, caso

