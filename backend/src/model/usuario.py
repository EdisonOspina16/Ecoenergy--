import sys
sys.path.append("src")
from datetime import datetime

class Usuario:
    def __init__(self, id_usuario, nombre,apellidos, correo, contraseña, fecha_registro=None):

        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellidos = apellidos
        self.correo = correo
        self.contraseña = contraseña
        self.fecha_registro = fecha_registro if fecha_registro else datetime.now()


    def to_dict(self):

        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "contraseña": self.contraseña,
            "fecha_registro": self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def __repr__(self):

        return f"< Usuario {self.nombre} - {self.correo} >"
