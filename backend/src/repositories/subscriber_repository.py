from src.domain.errors import PersistenciaError, CorreoDuplicadoError
from psycopg2 import Error as DatabaseError


class SubscriberRepository:

    def __init__(self, conexion):
        self.conn = conexion

    def crear_suscriptor(self, email: str) -> bool:
        """
        Inserta un nuevo suscriptor en la BD.
        Retorna True si se insertó correctamente.
        Lanza CorreoDuplicadoError si el correo ya existe.
        Lanza PersistenciaError ante cualquier otro error de BD.
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO subscribers (email)
                VALUES (%s)
            """, (email,))
            self.conn.commit()
            cur.close()
            return True

        except DatabaseError as e:
            self.conn.rollback()
            if "duplicate" in str(e).lower():
                raise CorreoDuplicadoError("Correo ya registrado")
            raise PersistenciaError(f"Error en base de datos: {e}")