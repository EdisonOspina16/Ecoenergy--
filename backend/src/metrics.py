from flask import request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# ============================================
# 📊 DEFINICIÓN DE MÉTRICAS
# ============================================

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Número total de solicitudes HTTP",
    ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY_SECONDS = Histogram(
    "request_latency_seconds",
    "Latencia de solicitudes HTTP en segundos",
    ["endpoint"]
)

ERRORS_TOTAL = Counter(
    "http_errors_total",
    "Número total de respuestas con error (4xx o 5xx)",
    ["endpoint", "status_code"]
)


# ============================================
# 🔧 CONFIGURACIÓN DE MÉTRICAS
# ============================================

def setup_metrics(app):
    """Configura los hooks de métricas en la aplicación Flask"""
    
    @app.before_request
    def before_request():
        if request.path == "/metrics":
            return
        request._metrics_timer = REQUEST_LATENCY_SECONDS.labels(
            endpoint=request.path
        ).time()

    @app.after_request
    def after_request(response):
        if request.path != "/metrics":
            if hasattr(request, "_metrics_timer"):
                request._metrics_timer.observe_duration()

            HTTP_REQUESTS_TOTAL.labels(
                method=request.method,
                endpoint=request.path,
                http_status=response.status_code
            ).inc()

            if 400 <= response.status_code < 600:
                ERRORS_TOTAL.labels(
                    endpoint=request.path,
                    status_code=response.status_code
                ).inc()

        return response

    @app.route("/metrics")
    def metrics():
        """Endpoint que expone las métricas en formato Prometheus"""
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    
    print("📊 Métricas de Prometheus configuradas correctamente")
