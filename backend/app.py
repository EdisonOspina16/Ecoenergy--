import sys
sys.path.append("src")
import webbrowser
from flask import Flask
from flask import render_template
from flask_cors import CORS  
from flasgger import Swagger
from src.routes import vista_usuarios



app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura_iper_iper_segura_ecoenergy_123'

#  Permitir peticiones desde Next.js (localhost:3000)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Inicializar Swagger
Swagger(app)

# Registramos los Blueprints
app.register_blueprint(vista_usuarios.blueprint)


if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000/apidocs/")
    app.run(host="0.0.0.0", debug=True, port=5000)  # aseguramos que corra en 5000
