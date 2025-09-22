import sys
sys.path.append("src")


from psycopg2.extras import RealDictCursor
from google import genai

from model.dispositivo import Dispositivo
from SecretConfig import GEMINI_API_KEY, GEMINI_PROMPT, GEMINI_MODEL
from src.database import obtener_conexion


# -----------------------------------------
# CRUD DISPOSITIVOS
# -----------------------------------------

def crear(nombre_producto, categoria, vatios):
    """
    Crea un nuevo dispositivo y lo retorna como objeto Dispositivo.
    """
    conn = obtener_conexion()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO dispositivo (nombre_producto, categoria, vatios) VALUES (%s, %s, %s) RETURNING id, fecha_creacion",
                    (nombre_producto, categoria, vatios)
                )
                fila = cur.fetchone()
                conn.commit()
                return Dispositivo(id=fila[0], nombre_producto=nombre_producto, categoria=categoria, vatios=vatios, fecha_creacion=fila[1])
        except Exception as e:
            print(f"Error al crear dispositivo: {e}")
        finally:
            conn.close()
    return None


def obtener_dispositivos():
    """
    Retorna una lista de objetos Dispositivo.
    """
    dispositivos = []
    try:
        conn = obtener_conexion()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM dispositivo")
        filas = cur.fetchall()

        for fila in filas:
            dispositivo = Dispositivo(
                id=fila['id'],
                nombre_producto=fila['nombre_producto'],
                categoria=fila['categoria'],
                vatios=fila['vatios'],
                fecha_creacion=fila['fecha_creacion']
            )
            dispositivos.append(dispositivo)

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al obtener dispositivos: {e}")
    return dispositivos


def obtener_dispositivo_por_id(id):
    """
    Obtiene un dispositivo por su ID.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM dispositivo WHERE id = %s", (id,))
        fila = cur.fetchone()

        cur.close()
        conn.close()

        if fila:
            return Dispositivo(
                id=fila['id'],
                nombre_producto=fila['nombre_producto'],
                categoria=fila['categoria'],
                vatios=fila['vatios'],
                fecha_creacion=fila['fecha_creacion']
            )
        return None
    except Exception as e:
        print(f"Error al obtener dispositivo por ID: {e}")
        return None


def actualizar_dispositivo(dispositivo: Dispositivo):
    """
    Actualiza la información de un dispositivo existente.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor()

        cur.execute("""
            UPDATE dispositivo
            SET nombre_producto = %s, categoria = %s, vatios = %s
            WHERE id = %s
        """, (dispositivo.nombre_producto, dispositivo.categoria, dispositivo.vatios, dispositivo.id))

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al actualizar dispositivo: {e}")
        return False


def eliminar_dispositivo(id):
    """
    Elimina un dispositivo por ID.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor()

        cur.execute("DELETE FROM dispositivo WHERE id = %s", (id,))
        conn.commit()

        if cur.rowcount == 0:
            cur.close()
            conn.close()
            return {'mensaje': 'Dispositivo no encontrado'}, 404
        
        cur.close()
        conn.close()
        return {'mensaje': 'Dispositivo eliminado exitosamente'}, 200
    
    except Exception as e:
        print(f"Error al eliminar dispositivo: {e}")
        return {'mensaje': 'Error al eliminar dispositivo'}, 500

# -----------------------------------------
# FUNCIONES DEL ADMIN
# -----------------------------------------


def crear_dispositivo(nombre_producto, categoria, vatios):
    if not nombre_producto or not categoria or not vatios:
        return {"error": "Todos los campos son obligatorios"}, 400
    
    try:
        vatios = int(vatios)
        if vatios <= 0:
            return {"error": "Los vatios deben ser un número positivo"}, 400
    except ValueError:
        return {"error": "Los vatios deben ser un número entero"}, 400
    
    dispositivo = crear(nombre_producto, categoria, vatios)
    if dispositivo:
        return dispositivo.to_dict(), 201
    return {"error": "Error al crear el dispositivo"}, 500


def actualizar_dispositivo(id, nombre_producto, categoria, vatios):
    dispositivo = obtener_dispositivo_por_id(id)
    if not dispositivo:
        return {"error": "Dispositivo no encontrado"}, 404
    
    try:
        vatios = int(vatios)
        if vatios <= 0:
            return {"error": "Los vatios deben ser un número positivo"}, 400
    except ValueError:
        return {"error": "Los vatios deben ser un número entero"}, 400
    
    dispositivo.nombre_producto = nombre_producto
    dispositivo.categoria = categoria
    dispositivo.vatios = vatios
    
    if dispositivo.actualizar():
        return dispositivo.to_dict(), 200
    return {"error": "Error al actualizar el dispositivo"}, 500


def calcular_consumo(dispositivos):
    consumo_diario_kwh = 0.0
    total_watts = 0
    dispositivos_datos = []

    for item in dispositivos:
        id_disp   = item.get('id')
        uso       = item.get('usage')
        unidad    = item.get('unit')

        disp = obtener_dispositivo_por_id(id_disp)
        if not disp:
            continue
        dispositivos_datos.append({
            "id": disp.id,
            "nombre_producto": disp.nombre_producto,
            "categoria": disp.categoria,
            "vatios": disp.vatios,
            "fecha_creacion": disp.fecha_creacion.isoformat()
        })

        vatios = disp.vatios
        total_watts += vatios

        # 1) convertir W a kW
        potencia_kw = vatios / 1000.0  # 1 kW = 1000 W 

        # 2) convertir minutos → horas
        horas_uso = uso / 60.0 if unidad == 'minutes' else uso

        # 3) kWh de este dispositivo por día
        consumo_diario_kwh += potencia_kw * horas_uso  # kW × h = kWh 

    if total_watts == 0 or consumo_diario_kwh == 0:
        return {"error": "No hay dispositivos o datos de uso válidos"}, 400

    consumo_mensual_kwh = round(consumo_diario_kwh * 30, 2)  # 30 días  
    return {
        "consumo_total_watts": total_watts,
        "consumo_diario_kwh": round(consumo_diario_kwh, 2),
        "consumo_mensual_kwh": consumo_mensual_kwh,
        "dispositivos_datos": dispositivos_datos
    }, 200


def obtener_dispositivos_por_categoria():
    dispositivos = obtener_dispositivos()
    productos_por_categoria = {}

    for dispositivo in dispositivos:
        categoria = dispositivo.categoria
        if categoria not in productos_por_categoria:
            productos_por_categoria[categoria] = []
        productos_por_categoria[categoria].append(dispositivo)
    return productos_por_categoria

def clasificar_texto(texto):
    client = genai.Client(api_key = GEMINI_API_KEY)  
  
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[texto]
    )

    return {"response": response.text}
