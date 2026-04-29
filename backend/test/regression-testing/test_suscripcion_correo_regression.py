import pytest
from flask import Flask
from unittest.mock import patch
from src.routes.vista_email import email_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(email_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@patch("src.routes.vista_email.send_welcome_email")
def test_regression_suscripcion_correo(mock_send, client, snapshot):
    """
    Prueba de regresión para Suscripción de correo.
    """
    payload = {
        "email": "newsletter@test.com"
    }

    response = client.post("/subscribe", json=payload)
    
    assert response.status_code == 200
    mock_send.assert_called_once_with("newsletter@test.com")
    assert response.json == snapshot
