import sys
sys.path.append("src")

from flask import Flask
from flask import render_template

from src.view_web import vista_usuarios
from src.view_web import vista_admin


app = Flask(__name__)

app.secret_key = 'clave_secreta_super_segura_iper_iper_segura_ecoenergy_123'


# Registramos los Blueprints que creamos 
app.register_blueprint(vista_usuarios.blueprint)
app.register_blueprint(vista_admin.bp_admin)

if __name__ == '__main__':
    
    
    app.run(debug=True)
