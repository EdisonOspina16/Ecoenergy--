import pytest
import time
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock, patch
from hamcrest import assert_that, less_than

# Mocks necesarios para inicializar la app sin dependencias externas bloqueantes
with patch("google.genai.Client") as FakeClient:
    fake_models = Mock()
    fake_models.generate_content.return_value = Mock(text="{}")
    FakeClient.return_value = Mock(models=fake_models)
    from app import app

@pytest.fixture(scope="module")
def setup_app():
    """Configura la aplicación Flask en modo testing."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "testing-secret"
    with app.app_context():
        yield app

def send_login_request(app_instance, email, password):
    """Función auxiliar para enviar una petición HTTP al endpoint de login."""
    start_time = time.time()
    # Usar test_client como un context manager asegura independencia de sesiones
    with app_instance.test_client() as client:
        response = client.post("/login", json={
            "correo": email,
            "contrasena": password
        })
    latency = time.time() - start_time
    return response.status_code, latency

@pytest.mark.performance
def test_load_login(setup_app):
    """
    Prueba de Carga (Load Testing) con Pytest.
    Valida el funcionamiento bajo una carga de usuarios esperada o normal.
    Simulamos una cantidad moderada de usuarios haciendo peticiones concurrentes.
    """
    users_count = 50
    latencies = []
    
    # ThreadPoolExecutor permite hacer las peticiones concurrentemente
    with ThreadPoolExecutor(max_workers=users_count) as executor:
        futures = [
            executor.submit(send_login_request, setup_app, "loadtest@ecoenergy.com", "Edison#101") 
            for _ in range(users_count)
        ]
        
        for future in futures:
            status, latency = future.result()
            latencies.append(latency)

    avg_latency = sum(latencies) / len(latencies)
    print(f"\n[Load Test] Promedio de latencia para {users_count} usuarios concurrentes: {avg_latency:.4f} s")
    
    # Aserción: el tiempo promedio debe ser menor a 2.0 segundos para una carga normal
    assert_that(avg_latency, less_than(2.0))
