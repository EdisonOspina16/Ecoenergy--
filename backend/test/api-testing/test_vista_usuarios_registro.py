import pytest
from flask import Flask
from unittest.mock import patch
from hamcrest import assert_that, is_, equal_to

# Importamos el blueprint y constantes necesarios
from src.routes.vista_usuarios import blueprint_Usuarios, ERROR_CAMPOS_REQUERIDOS

@pytest.fixture
def app():
    """Fixture para crear la aplicación Flask de prueba (Setup general)."""
    app = Flask(__name__)
    app.register_blueprint(blueprint_Usuarios)
    return app

@pytest.fixture
def client(app):
    """Fixture para obtener el cliente HTTP de pruebas."""
    return app.test_client()

# --- CASO 1: Camino Normal (Éxito) ---
@patch('src.routes.vista_usuarios.registrar_usuario')
def test_registro_exitoso(mock_registrar_usuario, client):
    """
    Prueba el registro exitoso del usuario. 
    Se espera que responda HTTP 200 y devuelva el mensaje de éxito.
    """
    # [Arrange] - Preparar
    # Dummy: Datos ficticios necesarios para pasar las validaciones del endpoint.
    dummy_data = {
        'nombre': 'Juan',
        'apellidos': 'Perez',
        'correo': 'juan.perez@ejemplo.com',
        'contrasena': 'secreta123'
    }
    
    # Stub: Configuramos el mock para que retorne "True", simulando éxito en la BD.
    mock_registrar_usuario.return_value = True

    # [Act] - Actuar
    response = client.post('/registro', json=dummy_data)

    # [Assert] - Afirmar
    assert_that(response.status_code, is_(200))
    assert_that(response.get_json(), equal_to({
        "message": "Usuario registrado con éxito",
        "redirect": "/login"
    }))
    
    # Mock (Verificación de interacciones): Afirmamos que el servicio subyacente 
    # se llamó exactamente 1 vez y recibió los datos correctos del Dummy.
    mock_registrar_usuario.assert_called_once_with(
        nombre='Juan',
        apellidos='Perez',
        correo='juan.perez@ejemplo.com',
        contrasena='secreta123'
    )

# --- CASO 2: Caso Borde (Faltan campos) ---
def test_registro_error_faltan_campos(client):
    """
    Prueba la validación cuando se recibe un JSON incompleto.
    Se espera HTTP 400 y mensaje de 'Faltan campos requeridos'.
    """
    # [Arrange]
    # Dummy Data: Faltan campos (ej: no está 'contrasena')
    incompleta_data = {
        'nombre': 'Maria',
        'apellidos': 'Gomez',
        'correo': 'maria@ejemplo.com'
    }

    # [Act]
    response = client.post('/registro', json=incompleta_data)

    # [Assert]
    assert_that(response.status_code, is_(400))
    assert_that(response.get_json(), equal_to(ERROR_CAMPOS_REQUERIDOS))

# --- CASO 3: Caso Borde (Body/payload completamente vacío) ---
def test_registro_error_payload_vacio(client):
    """
    Prueba la validación cuando no se envía ningún JSON.
    Se espera HTTP 400.
    """
    # [Arrange] - No enviamos JSON
    
    # [Act]
    response = client.post('/registro', json={})

    # [Assert]
    assert_that(response.status_code, is_(400))
    assert_that(response.get_json(), equal_to(ERROR_CAMPOS_REQUERIDOS))

# --- CASO 4: Caso Error (Falla el registro en Base de Datos) ---
@patch('src.routes.vista_usuarios.registrar_usuario')
def test_registro_error_guardar_bd(mock_registrar_usuario, client):
    """
    Prueba el escenario en el cual registrar_usuario falla (ej: correo ya registrado).
    Se espera HTTP 500 y un mensaje de error genérico.
    """
    # [Arrange]
    dummy_data = {
        'nombre': 'Carlos',
        'apellidos': 'Ruiz',
        'correo': 'carlos.r@ejemplo.com',
        'contrasena': 'mi_password'
    }
    
    # Stub: Simulamos que la inserción de usuario falla (retorna False)
    mock_registrar_usuario.return_value = False

    # [Act]
    response = client.post('/registro', json=dummy_data)

    # [Assert]
    assert_that(response.status_code, is_(500))
    assert_that(response.get_json(), equal_to({"error": "Error al registrar usuario"}))
    
    # Mock: Se debe seguir llamando a la BD aunque falló
    mock_registrar_usuario.assert_called_once_with(**dummy_data)
