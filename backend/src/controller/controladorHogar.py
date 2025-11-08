import sys
sys.path.append("src")

from psycopg2.extras import RealDictCursor
from model.hogar import Hogar
from src.database import obtener_conexion


def obtener_hogar_por_usuario(id_usuario):
    """
    Obtiene el hogar asociado a un usuario específico.
    """
    try:
        conn = obtener_conexion()
        if not conn:
            return None
            
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT id_hogar, id_usuario, direccion, nombre_hogar
            FROM hogares 
            WHERE id_usuario = %s
            LIMIT 1
        """, (id_usuario,))
        
        fila = cur.fetchone()
        cur.close()
        conn.close()
        
        if fila:
            return Hogar(
                id_hogar=fila['id_hogar'],
                id_usuario=fila['id_usuario'],
                direccion=fila['direccion'],
                nombre_hogar=fila['nombre_hogar']
            )
        return None
    except Exception as e:
        print(f"Error al obtener hogar: {e}")
        return None


def crear_hogar(id_usuario, direccion, nombre_hogar):
    """
    Crea un nuevo hogar para un usuario.
    """
    try:
        conn = obtener_conexion()
        if not conn:
            return None
            
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            INSERT INTO hogares (id_usuario, direccion, nombre_hogar)
            VALUES (%s, %s, %s)
            RETURNING id_hogar, id_usuario, direccion, nombre_hogar
        """, (id_usuario, direccion, nombre_hogar))
        
        fila = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        if fila:
            return Hogar(
                id_hogar=fila['id_hogar'],
                id_usuario=fila['id_usuario'],
                direccion=fila['direccion'],
                nombre_hogar=fila['nombre_hogar']
            )
        return None
    except Exception as e:
        print(f"Error al crear hogar: {e}")
        return None


def actualizar_hogar(id_usuario, direccion, nombre_hogar):
    """
    Actualiza el hogar existente de un usuario.
    """
    try:
        conn = obtener_conexion()
        if not conn:
            return None
            
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            UPDATE hogares 
            SET direccion = %s, 
                nombre_hogar = %s
            WHERE id_usuario = %s
            RETURNING id_hogar, id_usuario, direccion, nombre_hogar
        """, (direccion, nombre_hogar, id_usuario))
        
        fila = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        if fila:
            return Hogar(
                id_hogar=fila['id_hogar'],
                id_usuario=fila['id_usuario'],
                direccion=fila['direccion'],
                nombre_hogar=fila['nombre_hogar']
            )
        return None
    except Exception as e:
        print(f"Error al actualizar hogar: {e}")
        return None


def crear_o_actualizar_hogar(id_usuario, direccion, nombre_hogar):
    """
    Crea o actualiza el hogar de un usuario según si ya existe.
    """
    hogar_existente = obtener_hogar_por_usuario(id_usuario)
    
    if hogar_existente:
        return actualizar_hogar(id_usuario, direccion, nombre_hogar)
    else:
        return crear_hogar(id_usuario, direccion, nombre_hogar)