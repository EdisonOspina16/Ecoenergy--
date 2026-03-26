from src.domain.errors import PersistenciaError
from psycopg2 import Error as DatabaseError
from psycopg2.extras import RealDictCursor


class DispositivoRepository:

    def __init__(self, conexion):
        self.conn = conexion

#listar dispositivo
    def obtener_por_usuario(self, id_usuario: int) -> list:
        """
        Retorna las filas crudas de dispositivos asociados al hogar de un usuario.
        Retorna lista vacía si el usuario no tiene dispositivos.
        Lanza PersistenciaError ante cualquier error de base de datos.
        """
        try:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                SELECT d.id_dispositivos, d.id_hogar, d.alias, d.id_dispositivo_iot,
                       d.tipo_dispositivo_ia, d.estado_activo, d.fecha_conexion
                FROM dispositivos d
                INNER JOIN hogares h ON d.id_hogar = h.id_hogar
                WHERE h.id_usuario = %s
                ORDER BY d.fecha_conexion DESC
            """, (id_usuario,))

            filas = cur.fetchall()
            cur.close()
            return filas

        except DatabaseError as e:
            raise PersistenciaError(f"Error en base de datos: {e}")
        
#mostrar estado dispositivo

    def obtener_dispositivos_con_consumo(self) -> list:
        """
        Retorna las filas crudas de todos los dispositivos con su último
        consumo registrado. Sin filtro por usuario.
        Formato de cada fila: (alias, watts, estado_activo, tipo_dispositivo_ia)
        Lanza PersistenciaError ante cualquier error de base de datos.
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT DISTINCT ON (d.id_dispositivos)
                    d.alias,
                    r.watts,
                    d.estado_activo,
                    d.tipo_dispositivo_ia
                FROM dispositivos AS d
                LEFT JOIN registros_consumo AS r
                    ON r.id_dispositivo = d.id_dispositivos
                ORDER BY d.id_dispositivos, r.fecha_hora DESC
            """)
 
            filas = cur.fetchall()
            cur.close()
            return filas
 
        except DatabaseError as e:
            raise PersistenciaError(f"Error en base de datos: {e}")