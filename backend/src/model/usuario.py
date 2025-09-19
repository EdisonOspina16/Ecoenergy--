import sys
sys.path.append("src")
from datetime import datetime

class Usuario:
    def __init__(self, id, nombre, correo, contraseña, es_admin, fecha_registro=None,
                 telefono=None, direccion=None, ciudad=None, estrato=None):

        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.contraseña = contraseña
        self.es_admin = es_admin
        self.fecha_registro = fecha_registro if fecha_registro else datetime.now()
        self.telefono = telefono
        self.direccion = direccion
        self.ciudad = ciudad
        self.estrato = estrato

    def to_dict(self):

        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "contraseña": self.contraseña,
            "es_admin": self.es_admin,
            "fecha_registro": self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
            "telefono": self.telefono,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "estrato": self.estrato
        }

    def __repr__(self):

        return f"<Usuario {self.nombre} - {self.correo} - Tel: {self.telefono}>"
