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

def run_batch(app_instance, user_count):
    """Ejecuta un lote de peticiones concurrentes y devuelve la latencia promedio."""
    latencies = []
    with ThreadPoolExecutor(max_workers=user_count) as executor:
        futures = [
            executor.submit(send_login_request, app_instance, "spiketest@ecoenergy.com", "Edison#101") 
            for _ in range(user_count)
        ]
        for future in futures:
            _, lat = future.result()
            latencies.append(lat)
    return sum(latencies) / len(latencies) if latencies else 0

@pytest.mark.performance
def test_spike_login(setup_app):
    """
    Prueba de Picos (Spike Testing) con Pytest.
    Mide la reacción del sistema ante aumentos repentinos y masivos de usuarios.
    Se verifica que el sistema pueda recuperarse después de que el pico pasa.
    """
    
    # Etapa 1: Carga normal (Ej. 20 usuarios concurrentes)
    normal_lat_1 = run_batch(setup_app, 20)
    
    # Etapa 2: Pico repentino (Ej. 150 usuarios concurrentes)
    spike_lat = run_batch(setup_app, 150)
    
    # Etapa 3: Vuelta a la normalidad (Ej. 20 usuarios concurrentes)
    normal_lat_2 = run_batch(setup_app, 20)

    print(f"\n[Spike Test] Latencia Normal 1: {normal_lat_1:.4f} s | Latencia Pico: {spike_lat:.4f} s | Latencia Normal 2: {normal_lat_2:.4f} s")
    
    # Aserción: El sistema debe mantener buenos tiempos en carga normal y, 
    # crucialmente, debe recuperar esos buenos tiempos después del pico.
    assert_that(normal_lat_1, less_than(2.0))
    assert_that(normal_lat_2, less_than(2.0))
    # Aunque la latencia en el pico sea mayor, el hecho de que se pueda procesar normal_lat_2
    # demuestra la estabilidad del sistema.
