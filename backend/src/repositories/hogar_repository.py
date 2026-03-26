from src.domain.errors import PersistenciaError
from psycopg2 import Error as DatabaseError
from psycopg2.extras import RealDictCursor


class HogarRepository:

    def __init__(self, conexion):
        self.conn = conexion

    def crear_hogar(self, id_usuario: int, direccion: str, nombre_hogar: str) -> dict | None:
        """
        Inserta un nuevo hogar en la BD y retorna la fila cruda creada.
        Retorna None si no se insertó ninguna fila.
        Lanza PersistenciaError ante cualquier error de base de datos.
        """
        try:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                INSERT INTO hogares (id_usuario, direccion, nombre_hogar)
                VALUES (%s, %s, %s)
                RETURNING id_hogar, id_usuario, direccion, nombre_hogar
            """, (id_usuario, direccion, nombre_hogar))

            fila = cur.fetchone()
            self.conn.commit()
            cur.close()
            return fila

        except DatabaseError as e:
            self.conn.rollback()
            raise PersistenciaError(f"Error en base de datos: {e}")