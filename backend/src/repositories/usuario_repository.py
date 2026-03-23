from src.model.hogar import Hogar
from src.domain.errors import PersistenciaError, CorreoDuplicadoError
from psycopg2 import Error as DatabaseError
from psycopg2.extras import RealDictCursor


class UsuarioRepository:

    def __init__(self, conexion):
        self.conn = conexion

    def crear_usuario(self, nombre, apellidos, correo, hash_contrasena):
        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO usuarios (nombre, apellidos, correo, contrasena)
                VALUES (%s, %s, %s, %s)
            """, (nombre, apellidos, correo, hash_contrasena))

            self.conn.commit()

        except DatabaseError as e:
            self.conn.rollback()

            if "duplicate" in str(e).lower():
                raise CorreoDuplicadoError("El correo ya está registrado")

            raise PersistenciaError(f"Error en base de datos: {e}")


    def obtener_hogar_por_usuario(self, id_usuario: int) -> Hogar | None:
        """
        Obtiene el hogar asociado a un usuario específico.
        """
        try:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                SELECT id_hogar, id_usuario, direccion, nombre_hogar
                FROM hogares
                WHERE id_usuario = %s
                LIMIT 1
            """, (id_usuario,))

            fila = cur.fetchone()
            cur.close()

            if fila:
                return Hogar(
                    id_hogar=fila['id_hogar'],
                    id_usuario=fila['id_usuario'],
                    direccion=fila['direccion'],
                    nombre_hogar=fila['nombre_hogar']
                )
            return None

        except DatabaseError as e:
            raise PersistenciaError(f"Error al obtener hogar: {e}")
