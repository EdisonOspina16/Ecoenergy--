import sys
sys.path.append("src")

from flask import Flask
from flask_cors import CORS

from src.routes import vista_usuarios
from src.routes.vista_perfil import blueprint_perfil  


app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura_iper_iper_segura_ecoenergy_123'

# Permitir peticiones desde Next.js (localhost:3000)
CORS(app, 
     resources={r"/*": {"origins": "http://localhost:3000"}},
     supports_credentials=True)  # Importante para que funcionen las sesiones

# Registramos los Blueprints
app.register_blueprint(vista_usuarios.blueprint)
app.register_blueprint(blueprint_perfil)  # Registrar el blueprint de perfil


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)