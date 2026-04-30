# EcoEnergy

EcoEnergy es una plataforma web para monitorear consumo eléctrico en el hogar, administrar tomacorrientes/dispositivos IoT, estimar ahorro energético y generar recomendaciones de eficiencia con apoyo de IA.

El proyecto está compuesto por:

- **Frontend:** aplicación Next.js con React y TypeScript.
- **Backend:** API REST en Flask.
- **Base de datos:** PostgreSQL.
- **IoT/simulación:** Mosquitto MQTT y simulación de consumo.
- **Observabilidad:** Prometheus y Grafana.
- **Calidad:** pruebas unitarias, API, regresión, seguridad, rendimiento y Screenplay/BDD.
- **CI/CD:** Jenkinsfiles separados para backend, frontend y pipeline general.

## Estado actual del proyecto

### Funcionalidades principales

- Registro de usuarios.
- Inicio y cierre de sesión con sesiones Flask.
- Cambio/recuperación de contraseña.
- Perfil de hogar con nombre y dirección.
- Registro, edición, conexión/desconexión y eliminación de tomacorrientes.
- Listado de dispositivos asociados al hogar.
- Dashboard/home con consumo total, consumo histórico y dispositivos.
- Recomendación diaria de ahorro.
- Cálculo de ahorro financiero, impacto ambiental e indicador didáctico.
- Métricas Prometheus expuestas desde Flask en `/metrics`.
- Simulación de datos de consumo para alimentar la experiencia del dashboard.

### Funcionalidad en revisión

- La suscripción por correo (`POST /subscribe`) existe, pero actualmente depende del envío SMTP real. Si las credenciales de correo no están configuradas correctamente, el frontend muestra error interno del servidor. Por eso el escenario E2E de frontend para suscripción fue retirado de la suite Screenplay.

## Arquitectura

```text
Ecoenergy/
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── src/
│   │   ├── aplication/
│   │   │   ├── service/
│   │   │   └── validators/
│   │   ├── controller/
│   │   ├── domain/
│   │   ├── infrastructure/ia/
│   │   ├── model/
│   │   ├── repositories/
│   │   ├── routes/
│   │   ├── database.py
│   │   ├── metrics.py
│   │   └── SecretConfig.py
│   └── test/
│       ├── api-testing/
│       ├── performance-testing/
│       ├── regression-testing/
│       ├── screenplay/
│       ├── security-testing/
│       └── unit-testing/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── src/
│   │   ├── app/
│   │   ├── hooks/
│   │   ├── lib/
│   │   └── styles/
│   └── test/
│       ├── api-testing/
│       ├── performance-testing/
│       ├── regression-testing/
│       ├── screenplay/
│       ├── security-testing/
│       └── unit-testing/
├── init-db/
├── mosquitto/
├── prometheus/
├── docker-compose.yml
├── docker-compose.jenkins.yml
├── Jenkinsfile
├── Jenkinsfile.backend
└── Jenkinsfile.frontend
```

## Stack técnico

### Backend

- Python 3.12
- Flask 3
- Flask-CORS
- PostgreSQL con `psycopg2`
- Prometheus Flask Exporter
- Google GenAI/Gemini
- Pytest
- Locust
- Bandit
- pip-audit
- Syrupy snapshots
- PyHamcrest

### Frontend

- Next.js
- React 18
- TypeScript
- CSS Modules
- Vitest
- Testing Library
- Playwright
- Cucumber.js
- ts-node

### Infraestructura

- Docker y Docker Compose
- PostgreSQL
- Eclipse Mosquitto
- Prometheus
- Grafana
- Jenkins

## Servicios y puertos

| Servicio             | Puerto local | Descripción                                 |
| -------------------- | -----------: | ------------------------------------------- |
| Frontend local       |       `3000` | Next.js en modo desarrollo                  |
| Frontend Docker      |       `3001` | Contenedor frontend, mapea a `3000` interno |
| Backend              |       `5000` | API Flask                                   |
| Backend extra        |       `8000` | Puerto adicional expuesto por compose       |
| PostgreSQL           |       `5432` | Base de datos                               |
| Mosquitto MQTT       |       `1883` | Broker MQTT                                 |
| Mosquitto WebSockets |       `9001` | MQTT por WebSockets                         |
| Prometheus           |       `9090` | Métricas                                    |
| Grafana              |       `3002` | Dashboards                                  |

## Configuración

### Variables y configuración del frontend

El frontend usa:

```bash
NEXT_PUBLIC_API_URL=http://localhost:5000
```

Si no se define, la aplicación usa `http://localhost:5000` por defecto desde:

- `frontend/src/lib/config/api.ts`
- `frontend/config.ts`

### Variables de pruebas Screenplay frontend

Las pruebas E2E de frontend leen:

```bash
E2E_BASE_URL=http://localhost:3000
E2E_EMAIL=tomasra@gmail.com
E2E_PASSWORD=Contrasena123.
E2E_BROWSER=chromium
HEADLESS=true
```

Todos tienen valor por defecto en `frontend/test/screenplay/support/env.ts`.

### Configuración del backend

El backend obtiene credenciales desde `backend/src/SecretConfig.py`.

Cuando corre en Docker:

```bash
DOCKER=1
PGHOST=db
PGDATABASE=ecoenergydb
PGUSER=ecoenergy
PGPASSWORD=ecoenergy123
```

Cuando corre fuera de Docker, `SecretConfig.py` usa la configuración remota definida allí.

También contiene la configuración de:

- SMTP para `POST /subscribe`.
- Gemini (`GEMINI_API_KEY`, `GEMINI_MODEL`).

> Importante: en un entorno real, estas credenciales deberían moverse a variables de entorno o un gestor de secretos.

## Ejecutar con Docker Compose

Desde la raíz del proyecto:

```bash
docker compose up -d --build
```

Verificar contenedores:

```bash
docker ps
```

Servicios esperados:

- `frontend`
- `backend`
- `db`
- `mosquitto`
- `prometheus`
- `grafana`

URLs principales:

- Frontend: `http://localhost:3001`
- Backend: `http://localhost:5000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3002`

Para detener todo:

```bash
docker compose down
```

Para detener y borrar volúmenes:

```bash
docker compose down -v
```

## Ejecutar en local sin Docker

### 1. Base de datos

Debes tener PostgreSQL disponible y las tablas creadas. Los scripts están en:

- `init-db/tablas.sql`
- `init-db/add_recomendacion_ahorro_diaria.sql`

Docker las crea automáticamente al levantar el servicio `db`.

### 2. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

El backend queda en:

```text
http://localhost:5000
```

### 3. Frontend

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

El frontend queda en:

```text
http://localhost:3000
```

## Frontend

### Páginas

| Ruta         | Descripción                                                              |
| ------------ | ------------------------------------------------------------------------ |
| `/`          | Landing principal con información de EcoEnergy, impacto, comunidad y CTA |
| `/login`     | Inicio de sesión                                                         |
| `/registro`  | Registro de usuario                                                      |
| `/recuperar` | Cambio/recuperación de contraseña                                        |
| `/dashboard` | Vista de usuario autenticado                                             |
| `/home`      | Panel principal de consumo, gráficos, dispositivos y recomendaciones     |
| `/perfil`    | Perfil del hogar y administración de tomacorrientes                      |

### Hooks principales

- `useLogin`
- `useRegistro`
- `useRecuperar`
- `useSubscribe`
- `useDispositivos`
- `useDeviceRegistration`
- `useProfileSubmit`

### Cliente HTTP y API

La capa de API está en `frontend/src/lib/api/`:

- `auth.ts`
- `registro.ts`
- `recuperar.ts`
- `profile.ts`
- `devices.ts`
- `dispositivos.ts`
- `subscribe.ts`

El helper compartido para JSON está en:

- `frontend/src/lib/http/jsonClient.ts`

## Backend

### Blueprints registrados

El archivo `backend/app.py` registra:

- `vista_usuarios`
- `vista_perfil`
- `vista_consumo`
- `email`
- `vista_dispositivos`

También inicializa:

- CORS para `http://localhost:3000` y `http://localhost:3001`
- sesiones Flask
- métricas Prometheus
- simulación de consumo al arrancar la aplicación

### Endpoints principales

| Método   | Endpoint                                    | Descripción                                                  |
| -------- | ------------------------------------------- | ------------------------------------------------------------ |
| `POST`   | `/registro`                                 | Registra usuario                                             |
| `POST`   | `/login`                                    | Inicia sesión y guarda usuario en sesión Flask               |
| `POST`   | `/logout`                                   | Cierra sesión                                                |
| `POST`   | `/recuperar`                                | Cambia contraseña                                            |
| `GET`    | `/perfil`                                   | Obtiene hogar y dispositivos del usuario autenticado         |
| `POST`   | `/perfil`                                   | Crea/actualiza perfil o registra tomacorriente según payload |
| `PUT`    | `/perfil/dispositivo/<id>`                  | Actualiza alias del dispositivo                              |
| `DELETE` | `/perfil/dispositivo/<id>`                  | Elimina dispositivo                                          |
| `PUT`    | `/perfil/dispositivo/<id>/estado`           | Cambia estado activo/inactivo                                |
| `GET`    | `/home`                                     | Retorna consumo total del último día                         |
| `GET`    | `/consumo-historico?rango=day\|week\|month` | Retorna serie histórica de consumo                           |
| `GET`    | `/dispositivos`                             | Lista dispositivos con consumo y estado                      |
| `GET`    | `/ahorro-estimado`                          | Calcula ahorro/impacto/indicador                             |
| `POST`   | `/recomendacion`                            | Genera recomendación a partir de consumo y dispositivo       |
| `GET`    | `/recomendacion-diaria`                     | Obtiene recomendación diaria del hogar autenticado           |
| `POST`   | `/recomendacion-diaria/generar`             | Genera y guarda recomendación diaria                         |
| `POST`   | `/subscribe`                                | Envía correo de bienvenida a suscriptor                      |
| `GET`    | `/metrics`                                  | Métricas Prometheus                                          |

### Modelo de datos

La base de datos se inicializa con:

- `usuarios`
- `hogares`
- `dispositivos`
- `registros_consumo`
- `recomendaciones`
- `recomendacion_ahorro_diaria`
- `subscribers`

## Flujos de usuario

### Registro e inicio de sesión

1. El usuario entra a `/registro`.
2. Ingresa nombre, apellidos, correo y contraseña.
3. La app llama a `POST /registro`.
4. Si el registro es exitoso, redirige a `/login`.
5. El usuario inicia sesión.
6. La app llama a `POST /login`.
7. El backend guarda la sesión y responde con redirección a `/home`.

### Perfil del hogar

1. El usuario inicia sesión.
2. Entra a `/perfil`.
3. Crea o actualiza nombre del hogar y dirección.
4. La app llama a `POST /perfil`.
5. El backend crea o actualiza el hogar del usuario autenticado.

### Gestión de tomacorrientes

1. El usuario crea su perfil de hogar.
2. Registra un tomacorriente con ID de dispositivo y apodo.
3. Puede cambiar alias, conectar/desconectar o eliminar.
4. La app usa los endpoints de `/perfil/dispositivo/...`.

### Home de consumo

1. El usuario entra a `/home`.
2. La app carga perfil, consumo total, histórico y dispositivos.
3. El consumo se actualiza periódicamente.
4. El usuario puede generar recomendaciones diarias de ahorro.

## Pruebas

### Backend

Desde `backend/`:

```bash
pytest
```

Ejecutar por carpeta:

```bash
pytest test/unit-testing
pytest test/api-testing
pytest test/regression-testing
pytest test/security-testing
pytest test/screenplay
```

Pruebas de rendimiento:

```bash
pytest test/performance-testing
```

El backend usa `pytest.ini` con:

- `pythonpath = . src`
- `testpaths = test`
- marcador `security`

### Frontend

Desde `frontend/`:

```bash
npm test
```

Modo watch:

```bash
npm run test:watch
```

CI con reporter compacto:

```bash
npm run test:ci
```

Screenplay/BDD:

```bash
npm run test:screenplay
```

La suite Screenplay de frontend usa Cucumber.js, Playwright y ts-node. Para ejecutarla correctamente, el frontend y backend deben estar corriendo, salvo pruebas que estén mockeadas a nivel de test.

Estado actual validado:

```text
12 scenarios (12 passed)
40 steps (40 passed)
```

## CI/CD

El repositorio incluye:

- `Jenkinsfile`: pipeline general.
- `Jenkinsfile.backend`: pipeline enfocado en backend.
- `Jenkinsfile.frontend`: pipeline enfocado en frontend.
- `docker-compose.jenkins.yml`: composición para entorno Jenkins.
- `Dockerfile.jenkins`: imagen auxiliar para Jenkins.

## Observabilidad

Prometheus se configura en:

- `prometheus/prometheus.yml`

Scrapea:

- `prometheus:9090`
- `backend:5000` en `/metrics`

Grafana se levanta desde Docker Compose en:

```text
http://localhost:3002
```

## Mosquitto MQTT

La configuración está en:

- `mosquitto/config/mosquitto.conf`

Puertos:

- `1883`: MQTT
- `9001`: WebSockets

La configuración permite conexiones anónimas y persistencia de datos/logs en volúmenes Docker.

## Scripts útiles

### Docker

```bash
docker compose up -d --build
docker compose logs -f backend
docker compose logs -f frontend
docker compose down
docker compose down -v
```

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
pytest
```

### Frontend

```bash
cd frontend
npm install
npm run dev
npm run build
npm start
npm test
npm run test:screenplay
```

## Solución de problemas

### CORS

- Verifica que el backend esté en `http://localhost:5000`.
- Verifica que el frontend esté en `http://localhost:3000` o `http://localhost:3001`.
- `backend/app.py` permite ambos orígenes.

### Sesión no se mantiene

- Las peticiones deben usar `credentials: "include"`.
- El backend usa cookies de sesión Flask con `SameSite=Lax`, `HttpOnly=True` y `Secure=False` para desarrollo local.

### Error de conexión a base de datos

- En Docker, revisa que `db` esté corriendo.
- En local, revisa credenciales de `SecretConfig.py`.
- Confirma que las tablas de `init-db/tablas.sql` existan.

### Frontend Docker abre en puerto distinto

En modo local con `npm run dev`, usa:

```text
http://localhost:3000
```

En Docker Compose, usa:

```text
http://localhost:3001
```

### Suscripción por correo falla

El endpoint `/subscribe` intenta enviar un correo real por SMTP. Si `EMAIL_CONFIG` no contiene credenciales válidas de aplicación, el backend puede responder error interno.

## Desarrolladores

- Ximena Ruíz
- Edison Ospina
- Ana Sofía
- Tomas Ramírez
- Juliana Alvarez
