# Instrucciones de Integración - EcoEnergy

## ✅ Funcionalidades Implementadas

### Backend (Flask)
- ✅ API REST para autenticación de usuarios
- ✅ Endpoints para login, registro, recuperar contraseña
- ✅ Configuración CORS para Next.js
- ✅ Manejo de sesiones con Flask

### Frontend (Next.js)
- ✅ Página de inicio (/) - Muestra mensaje del backend
- ✅ Página de login (/login) - Conectada con backend
- ✅ Página de registro (/registro) - Conectada con backend (formulario completo)
- ✅ Página de recuperar contraseña (/recuperar) - Conectada con backend
- ✅ Página de dashboard (/dashboard) - Para usuarios autenticados

## 🚀 Cómo Probar la Integración

### 1. Iniciar el Backend (Flask)
```bash
cd backend
pip install -r requirements.txt
python app.py
```
El backend estará disponible en: `http://localhost:5000`

### 2. Iniciar el Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
El frontend estará disponible en: `http://localhost:3000`

### 3. Probar las Funcionalidades

#### Página de Inicio (/)
- Muestra el mensaje del backend: "Hola Mundo, bienvenido a EcoEnergy"
- Si no hay usuario logueado, muestra botones para login/registro
- Si hay usuario logueado, muestra información del usuario

#### Login (/login)
1. Ingresa credenciales válidas
2. Si es exitoso, redirige a `/dashboard`
3. Si hay error, muestra mensaje de error

#### Registro (/registro)
1. Ingresa los datos básicos: nombre, apellidos, correo y contraseña
2. Todos los campos son obligatorios
3. Si es exitoso, redirige a `/login`

#### Recuperar Contraseña (/recuperar)
1. Ingresa correo y nueva contraseña
2. Si es exitoso, redirige a `/login`

#### Dashboard (/dashboard)
- Solo accesible para usuarios autenticados
- Muestra información del usuario
- Botón para cerrar sesión

## 🔧 Endpoints del Backend

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Mensaje de bienvenida |
| POST | `/login` | Iniciar sesión |
| POST | `/logout` | Cerrar sesión |
| POST | `/registro` | Registro completo |
| POST | `/recuperar` | Recuperar contraseña |
| GET | `/perfil` | Obtener perfil del usuario |

## 🎯 Flujo de Usuario

1. **Usuario nuevo**:
   - Visita `/` → Ve mensaje del backend
   - Hace clic en "Registrarse" → Va a `/registro`
   - Completa los datos básicos (nombre, apellidos, correo, contraseña) → Va a `/login`
   - Inicia sesión → Va a `/dashboard`

2. **Usuario existente**:
   - Visita `/` → Ve mensaje del backend
   - Hace clic en "Iniciar Sesión" → Va a `/login`
   - Inicia sesión → Va a `/dashboard`

3. **Usuario autenticado**:
   - Ve información personal en `/dashboard`
   - Puede cerrar sesión desde cualquier página

## 🐛 Solución de Problemas

### Error de CORS
- Verificar que el backend esté corriendo en puerto 5000
- Verificar que el frontend esté corriendo en puerto 3000
- El CORS está configurado para `http://localhost:3000`

### Error de Sesión
- Verificar que las peticiones incluyan `credentials: "include"`
- Verificar que el backend esté manejando las sesiones correctamente

### Error de Conexión
- Verificar que ambos servidores estén corriendo
- Verificar que no haya conflictos de puertos
- Revisar la consola del navegador para errores específicos

## 📝 Notas Importantes

- Las sesiones se mantienen entre páginas gracias a `credentials: "include"`
- El backend usa Flask sessions, no JWT tokens
- Todas las páginas manejan estados de carga y errores
- La UI es responsive y mantiene el estilo de EcoEnergy
