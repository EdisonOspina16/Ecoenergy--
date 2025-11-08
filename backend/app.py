import sys
sys.path.append("src")

from flask import Flask
from flask import render_template
from flask_cors import CORS

from src.routes import vista_usuarios



app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura_iper_iper_segura_ecoenergy_123'


# Permitir peticiones desde cualquier origen (solo para desarrollo/testing)
CORS(
    app,
    resources={r"/*": {
        "origins": [
            "http://localhost:3000",           # desarrollo local
            "http://192.168.49.2:30080",       # Minikube NodePort
            "http://localhost:30080",          # si usas kubectl port-forward
            # Si usas Ingress después, agrega tu dominio:
            # "https://ecoenergy.tudominio.com"
        ],
        "supports_credentials": True,          # ← CRUCIAL para cookies/sesiones
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }}
)

# Registramos los Blueprints
app.register_blueprint(vista_usuarios.blueprint)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)  # aseguramos que corra en 5000
