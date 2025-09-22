from datetime import datetime

class Dispositivo:
    def __init__(self, id=None, nombre_producto="", categoria= "", vatios=0, fecha_creacion= None):
        self.id = id
        self.nombre_producto = nombre_producto
        self.categoria = categoria
        self.vatios = vatios
        self.fecha_creacion = fecha_creacion if fecha_creacion else datetime.now() 

    def to_dict(self):
        return {
            "id": self.id,
            "nombre_producto": self.nombre_producto,
            "categoria": self.categoria,
            "vatios": self.vatios,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

    def __repr__(self):
        return f"<Dispositivo ID: {self.id}, Producto: {self.nombre_producto}, Categoria: {self.categoria}, Vatios: {self.vatios}, fecha_creacion: {self.fecha_creacion}>"
