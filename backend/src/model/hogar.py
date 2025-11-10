import sys
sys.path.append("src")

class Hogar:
    def __init__(self, id_hogar=None, id_usuario=None, direccion="", nombre_hogar=""):
        self.id_hogar = id_hogar
        self.id_usuario = id_usuario
        self.direccion = direccion
        self.nombre_hogar = nombre_hogar

    def to_dict(self):
        return {
            "id_hogar": self.id_hogar,
            "id_usuario": self.id_usuario,
            "direccion": self.direccion,
            "nombre_hogar": self.nombre_hogar
        }

    def __repr__(self):
        return f"<Hogar ID: {self.id_hogar}, Usuario: {self.id_usuario}, Nombre: {self.nombre_hogar}>"