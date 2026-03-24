from src.domain.errors import PersistenciaError, CorreoDuplicadoError
from psycopg2 import Error as DatabaseError


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
        
    def actualizar_contrasena(self, correo, nueva_hash) -> bool:
            """
            Actualiza la contraseña hasheada de un usuario identificado por correo.
            Retorna True si se actualizó al menos una fila, False si el correo
            no existe en la BD.
            Lanza PersistenciaError ante cualquier error de base de datos.
            """
            try:
                cur = self.conn.cursor()
                cur.execute("""
                    UPDATE usuarios
                    SET contrasena = %s
                    WHERE correo = %s
                """, (nueva_hash, correo))
    
                self.conn.commit()
                filas = cur.rowcount
                cur.close()
                return filas > 0
    
            except DatabaseError as e:
                self.conn.rollback()
                raise PersistenciaError(f"Error en base de datos: {e}")