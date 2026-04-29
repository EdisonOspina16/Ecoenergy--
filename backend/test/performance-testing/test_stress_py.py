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
    with app_instance.test_client() as client:
        response = client.post("/login", json={
            "correo": email,
            "contrasena": password
        })
    latency = time.time() - start_time
    return response.status_code, latency

@pytest.mark.performance
def test_stress_login(setup_app):
    """
    Prueba de Estrés (Stress Testing) con Pytest.
    Somete al sistema a cargas extremas para encontrar su punto de ruptura.
    Simulamos una gran cantidad de peticiones concurrentes superando la carga normal.
    """
    users_count = 200 # Una carga significativamente más alta que en Load Testing
    latencies = []

    # Limitamos los workers para no ahogar la máquina local que ejecuta los tests,
    # pero forzando un alto grado de concurrencia al mismo tiempo
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [
            executor.submit(send_login_request, setup_app, "stresstest@ecoenergy.com", "Edison#101") 
            for _ in range(users_count)
        ]
        
        for future in futures:
            status, latency = future.result()
            latencies.append(latency)

    avg_latency = sum(latencies) / len(latencies)
    print(f"\n[Stress Test] Promedio de latencia para {users_count} peticiones bajo estrés: {avg_latency:.4f} s")
    
    # Aserción: Bajo estrés, permitimos mayor latencia pero el sistema debe seguir respondiendo
    # Establecemos el límite en 5.0 segundos antes de considerar fallo total.
    assert_that(avg_latency, less_than(5.0))
