from src.database import obtener_conexion

def create_subscriber(email):
    conn = obtener_conexion()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO subscribers (email) VALUES (%s)",
            (email,)
        )
        conn.commit()
        return True
    except:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
