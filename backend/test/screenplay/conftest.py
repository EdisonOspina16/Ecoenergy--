from unittest.mock import Mock, patch

import pytest

from test.screenplay.actors.actor import Actor
from test.screenplay.actors.abilities import ApiClient

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


@pytest.fixture()
def actor(client):
    return Actor("Usuario").can(ApiClient(client))
