import sys
sys.path.append("src")

from flask import Flask
from flask_cors import CORS
from datetime import timedelta

from src.routes import vista_usuarios
from src.routes.vista_consumo import vista_consumo

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura_iper_iper_segura_ecoenergy_123'

# ============================================
# 🌐 CORS - Permitir peticiones desde Next.js
# ============================================
CORS(app, 
     resources={r"/*": {"origins": "http://localhost:3000"}},
     supports_credentials=True)

# ============================================
# 🍪 CONFIGURACIÓN DE SESIONES
# ============================================
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CORRECTO para localhost
app.config['SESSION_COOKIE_SECURE'] = False     # False porque estamos en HTTP
app.config['SESSION_COOKIE_HTTPONLY'] = True    # Protección contra XSS
app.config['SESSION_COOKIE_DOMAIN'] = None      # Importante para localhost
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # 1 hora

# ============================================
# 📋 REGISTRAR BLUEPRINTS
# ============================================
app.register_blueprint(vista_usuarios.blueprint)
app.register_blueprint(vista_consumo)

# ============================================
# 🚀 INICIAR APLICACIÓN
# ============================================
if __name__ == '__main__':
    print("="*60)
    print("🌱 EcoEnergy Backend - INICIANDO")
    print("="*60)
    print("📍 URL: http://localhost:5000")
    print("🍪 Sesiones: Configuradas (Duración: 1 hora)")
    print("🌐 CORS: Habilitado para http://localhost:3000")
    print("🔓 Credenciales: Permitidas")
    print("="*60)
    
    app.run(host="0.0.0.0", debug=True, port=5000)