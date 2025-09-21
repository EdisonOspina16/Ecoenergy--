import sys
sys.path.append("src")

from flask import Flask
from flask import render_template
from flask_cors import CORS

from src.routes import vista_usuarios



app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura_iper_iper_segura_ecoenergy_123'

#  Permitir peticiones desde Next.js (localhost:3000)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Registramos los Blueprints
app.register_blueprint(vista_usuarios.blueprint)


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # aseguramos que corra en 5000
