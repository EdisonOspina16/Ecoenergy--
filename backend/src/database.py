import sys
sys.path.append("src")

import psycopg2
from SecretConfig import PGHOST, PGDATABASE, PGUSER, PGPASSWORD, GEMINI_API_KEY, GEMINI_PROMPT, GEMINI_MODEL


def obtener_conexion():
    try:
        return psycopg2.connect(
            host=PGHOST,
            database=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD
        )
    except Exception as e:
        print("Error de conexión:", e)
        return None
