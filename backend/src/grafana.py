import sys
sys.path.append("src")

from flask import Flask, request, Response
from flask_cors import CORS

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from src.routes import vista_usuarios

from src.routes.vista_consumo import vista_consumo 
from src.controller.controlador_dis import iniciar_simulacion
from src.routes.vista_consumo import vista_consumo 

from src.routes.vista_consumo import vista_consumo



app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura_iper_iper_segura_ecoenergy_123'
app.register_blueprint(vista_consumo)
# Habilitar CORS para Next.js
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# -------------------------
# MÉTRICAS PARA PROMETHEUS
# -------------------------

# Contador de requests por método, endpoint y código de respuesta
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Número total de solicitudes HTTP",
    ["method", "endpoint", "http_status"]
)

# Histograma del tiempo de respuesta por endpoint
REQUEST_LATENCY_SECONDS = Histogram(
    "request_latency_seconds",
    "Latencia de solicitudes HTTP",
    ["endpoint"]
)


@app.before_request
def before_request():
    # iniciar temporizador
    request.start_time = REQUEST_LATENCY_SECONDS.labels(
        endpoint=request.path
    ).time()


@app.after_request
def after_request(response):
    # registrar duración de la solicitud
    try:
        request.start_time.observe_duration()
    except Exception:
        pass

    # contar la solicitud
    HTTP_REQUESTS_TOTAL.labels(
        method=request.method,
        endpoint=request.path,
        http_status=response.status_code
    ).inc()

    return response

def create_app():
    app = Flask(__name__)

    # Crear tablas en la base de datos
  
    # Registrar rutas
    app.register_blueprint(vista_consumo) 

    # Iniciar simulador
    iniciar_simulacion()

    @app.route('/')
    def index():
        return {"status": "Simulación en curso..."}

    return app


# -------------------------
# ENDPOINT /metrics
# -------------------------
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


# Registrar rutas
app.register_blueprint(vista_usuarios.blueprint)


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", debug=True, port=5000)
