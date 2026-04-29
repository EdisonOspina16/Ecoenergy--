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

def run_batch_endurance(app_instance, user_count):
    """Ejecuta peticiones concurrentes para una ronda específica de la prueba de resistencia."""
    latencies = []
    with ThreadPoolExecutor(max_workers=user_count) as executor:
        futures = [
            executor.submit(send_login_request, app_instance, "endurancetest@ecoenergy.com", "Edison#101") 
            for _ in range(user_count)
        ]
        for future in futures:
            _, lat = future.result()
            latencies.append(lat)
    return sum(latencies) / len(latencies) if latencies else 0

@pytest.mark.performance
def test_endurance_login(setup_app):
    """
    Prueba de Resistencia (Endurance Testing) con Pytest.
    Mantiene una carga constante por un tiempo prolongado para detectar fugas de memoria
    o degradación en el rendimiento.
    En contexto de CI, simulamos "prolongado" con múltiples rondas iterativas continuas.
    """
    rounds = 5 # Cantidad de iteraciones que simulan tiempo sostenido
    users_per_round = 30 # Carga constante en cada iteración
    latencies_per_round = []

    for i in range(rounds):
        lat = run_batch_endurance(setup_app, users_per_round)
        latencies_per_round.append(lat)
        # Una pequeña pausa entre rondas para simular peticiones intermitentes naturales
        time.sleep(0.5)

    avg_first_round = latencies_per_round[0]
    avg_last_round = latencies_per_round[-1]
    
    print(f"\n[Endurance Test] Latencia en Ronda 1: {avg_first_round:.4f} s | Latencia en Ronda {rounds}: {avg_last_round:.4f} s")
    
    # Aserción: La latencia no debe degradarse drásticamente hacia el final de la prueba.
    # El sistema debe ser capaz de procesar la última ronda sin perder eficiencia.
    # Aceptamos que el final pueda ser un poco más lento (ej. hasta 3 veces por saturación temporal),
    # pero nunca caer por un abismo de rendimiento.
    assert_that(avg_last_round, less_than(max(avg_first_round * 3, 2.0)))
