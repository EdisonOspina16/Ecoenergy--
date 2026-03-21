from sys import exc_info

import psycopg2
import pytest
from typing import Any
from src.aplication.service import usuario_service as us
from src.domain.errors import PersistenciaError, CorreoDuplicadoError
from psycopg2 import Error as DatabaseError

# ==============================================================
# INFRAESTRUCTURA DE PRUEBA (Objetos Dummy y Fixture)
# ==============================================================

class DummyCursor:
    """Cursor falso que simula INSERT y error de unicidad en correo."""

    def __init__(self) -> None:
        self.last_query: str | None = None
        self.last_params: tuple | None = None

    def execute(self, query: str, params: tuple) -> None:
        self.last_query = query
        self.last_params = params

        _, _, correo, _ = params

        if correo == "duplicado@gmail.com":
            raise DatabaseError("duplicate key value violates unique constraint")
        
        if correo == "error@gmail.com":
            raise psycopg2.Error("connection lost")

    def close(self) -> None:
        """limpia el estado del cursor (no hace nada en este dummy)"""
        pass
    

class DummyConnection:
    """Conexión falsa que registra commit y cierre."""

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

    def rollback(self):
        pass


@pytest.fixture(autouse=True)
def fake_db(monkeypatch: pytest.MonkeyPatch) -> DummyConnection:
    """
    Fixture compartido (Arrange global):
    - Reemplaza la conexión real a BD por DummyConnection.
    - Reemplaza generate_password_hash por una versión determinista.
    Se aplica automáticamente a todas las pruebas del módulo.
    """
    conn = DummyConnection()
    monkeypatch.setattr(us, "obtener_conexion", lambda: conn)
    monkeypatch.setattr(us, "generate_password_hash", lambda pwd: f"hashed-{pwd}")
    return conn


# ==============================================================
# PRUEBAS DE NOMBRE
# ==============================================================

def test_nombre_valido_simple() -> None:
    """CP-001: Un nombre con solo letras debe ser aceptado."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is True, "CP-001: Nombre válido simple debería retornar True"


def test_nombre_vacio() -> None:
    """CP-002: Un nombre vacío debe ser rechazado."""
    # Arrange
    nombre = ""
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-002: Nombre vacío debería retornar False"


def test_nombre_con_numeros() -> None:
    """CP-003: Un nombre que contiene dígitos debe ser rechazado."""
    # Arrange
    nombre = "Car1os"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-003: Nombre con números debería retornar False"


def test_nombre_dos_caracteres_minimo_valido() -> None:
    """CP-004: Un nombre de exactamente 2 caracteres está en el límite inferior válido."""
    # Arrange
    nombre = "Al"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is True, "CP-004: Nombre de 2 caracteres debería retornar True"


def test_nombre_51_caracteres_excede_maximo() -> None:
    """CP-005: Un nombre de 51 caracteres supera el máximo permitido."""
    # Arrange
    nombre = "A" * 51
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-005: Nombre de 51 caracteres debería retornar False"


# ==============================================================
# PRUEBAS DE APELLIDOS
# ==============================================================

def test_apellido_simple_valido() -> None:
    """CP-006: Un apellido con solo letras debe ser aceptado."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is True, "CP-006: Apellido simple válido debería retornar True"


def test_apellido_con_guion() -> None:
    """CP-007: Un apellido compuesto con guion debe ser aceptado."""
    # Arrange
    nombre = "Carlos"
    apellidos = "García-López"
    correo = "usuario@gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is True, "CP-007: Apellido con guion debería retornar True"


def test_apellido_vacio() -> None:
    """CP-008: Un apellido vacío debe ser rechazado."""
    # Arrange
    nombre = "Carlos"
    apellidos = ""
    correo = "usuario@gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-008: Apellido vacío debería retornar False"


def test_apellido_dos_caracteres_minimo_valido() -> None:
    """CP-009: Un apellido de exactamente 2 caracteres está en el límite inferior válido."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Go"
    correo = "usuario@gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is True, "CP-009: Apellido de 2 caracteres debería retornar True"


def test_apellido_nulo() -> None:
    """CP-010: Un apellido nulo (None) debe ser rechazado."""
    # Arrange
    nombre = "Carlos"
    apellidos = None
    correo = "usuario@gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-010: Apellido nulo debería retornar False"


# ==============================================================
# PRUEBAS DE CORREO
# ==============================================================

def test_correo_valido_estandar() -> None:
    """CP-011: Un correo con formato estándar debe ser aceptado."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is True, "CP-011: Correo válido estándar debería retornar True"


def test_correo_sin_arroba() -> None:
    """CP-012: Un correo sin @ debe ser rechazado."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuariogmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-012: Correo sin @ debería retornar False"


def test_correo_duplicado() -> None:
    """CP-013: Un correo ya registrado en la BD debe ser rechazado."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "duplicado@gmail.com"
    contrasena = "Abc123!@"

    # Act
    with pytest.raises(CorreoDuplicadoError) as exc_info:
        us.registrar_usuario(
            nombre=nombre,
            apellidos=apellidos,
            correo=correo,
            contrasena=contrasena,
        )
    
    # Assert
    assert "el correo ya está registrado" in str(exc_info.value).lower()


def test_error_generico_base_datos() -> None:
    """verificamos el manejo de un error genérico de base de datos (no relacionado con unicidad)
    durante la creación de usuario."""

    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "error@gmail.com"  # Este disparará error genérico
    contrasena = "Abc123!@"

    # Act
    with pytest.raises(PersistenciaError) as exc_info:
        us.registrar_usuario(
            nombre=nombre,
            apellidos=apellidos,
            correo=correo,
            contrasena=contrasena,
        )

    # Assert
    assert "error en base de datos" in str(exc_info.value).lower()


def test_correo_vacio() -> None:
    """CP-014: Un correo vacío debe ser rechazado."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = ""
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-014: Correo vacío debería retornar False"


def test_correo_mayor_254_caracteres() -> None:
    """CP-015: Un correo que supera 254 caracteres debe ser rechazado."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "u" * 245 + "@gmail.com"   # 255 caracteres en total
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-015: Correo >254 caracteres debería retornar False"


def test_correo_sin_dominio() -> None:
    """CP-016: Un correo sin dominio después del @ debe ser rechazado."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-016: Correo sin dominio debería retornar False"


def test_correo_sin_extension() -> None:
    """CP-017: Un correo sin extensión de dominio (sin .com, .co, etc.) debe ser rechazado."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-017: Correo sin extensión debería retornar False"


def test_correo_doble_arroba() -> None:
    """CP-018: Un correo con doble @ debe ser rechazado."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "user@@gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-018: Correo con doble @ debería retornar False"


def test_correo_con_espacios() -> None:
    """CP-019: Un correo que contiene espacios debe ser rechazado."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "user @gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-019: Correo con espacios debería retornar False"


def test_correo_con_mayusculas() -> None:
    """CP-020: Un correo con letras mayúsculas debe ser aceptado (case-insensitive)."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "Usuario@Gmail.COM"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is True, "CP-020: Correo con mayúsculas debería retornar True"


# ==============================================================
# PRUEBAS DE CONTRASEÑA
# ==============================================================

def test_contrasena_valida_fuerte() -> None:
    """CP-021: Una contraseña con mayúsculas, minúsculas, números y símbolos debe ser aceptada."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "Abc123!@"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is True, "CP-021: Contraseña válida fuerte debería retornar True"


def test_contrasena_solo_minusculas() -> None:
    """CP-022: Una contraseña sin mayúsculas ni caracteres especiales debe ser rechazada."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "abcdefgh"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-022: Contraseña solo minúsculas debería retornar False"


def test_contrasena_solo_numeros() -> None:
    """CP-023: Una contraseña compuesta únicamente de dígitos debe ser rechazada."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "12345678"

    # Act
    resultado =us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-023: Contraseña solo números debería retornar False"


def test_contrasena_solo_mayusculas() -> None:
    """CP-024: Una contraseña compuesta únicamente de mayúsculas debe ser rechazada."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "ABCDEFGH"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-024: Contraseña solo mayúsculas debería retornar False"


def test_contrasena_vacia() -> None:
    """CP-025: Una contraseña vacía debe ser rechazada."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = ""

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-025: Contraseña vacía debería retornar False"


def test_contrasena_nula() -> None:
    """CP-026: Una contraseña nula (None) debe ser rechazada."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = None

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-026: Contraseña nula debería retornar False"


def test_contrasena_menos_de_8_caracteres() -> None:
    """CP-027: Una contraseña con menos de 8 caracteres debe ser rechazada."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "Abc1!"   # 5 caracteres

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-027: Contraseña menor a 8 caracteres debería retornar False"


def test_contrasena_exactamente_8_caracteres() -> None:
    """CP-028: Una contraseña de exactamente 8 caracteres válidos debe ser aceptada (límite inferior)."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "Abc123!@"   # exactamente 8 caracteres

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is True, "CP-028: Contraseña de exactamente 8 caracteres debería retornar True"


def test_contrasena_con_espacios() -> None:
    """CP-029: Una contraseña que contiene espacios debe ser rechazada."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "Abc 123!"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-029: Contraseña con espacios debería retornar False"


def test_contrasena_caracteres_especiales_validos() -> None:
    """CP-030: Una contraseña con caracteres especiales válidos debe ser aceptada."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "P@ssw0rd#"

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is True, "CP-030: Contraseña con caracteres especiales válidos debería retornar True"


def test_contrasena_mayor_128_caracteres() -> None:
    """CP-031: Una contraseña de más de 128 caracteres debe ser rechazada."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "A" * 130   # 130 caracteres, supera el máximo

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-031: Contraseña >128 caracteres debería retornar False"


def test_contrasena_con_emoji() -> None:
    """CP-032: Una contraseña que contiene emojis debe ser rechazada."""
    # Arrange
    nombre = "Carlos"
    apellidos = "Gómez"
    correo = "usuario@gmail.com"
    contrasena = "Abc123\U0001f600"   # carácter fuera del rango ASCII permitido

    # Act
    resultado = us.registrar_usuario(
        nombre=nombre,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena,
    )

    # Assert
    assert resultado is False, "CP-032: Contraseña con emoji debería retornar False"