import sys
sys.path.append("src")
from datetime import datetime

class Dispositivo:
    def __init__(self, id_dispositivos=None, id_hogar=None, alias="", 
                 id_dispositivo_iot="", tipo_dispositivo_ia="", 
                 estado_activo=True, fecha_conexion=None):
        self.id_dispositivos = id_dispositivos
        self.id_hogar = id_hogar
        self.alias = alias
        self.id_dispositivo_iot = id_dispositivo_iot
        self.tipo_dispositivo_ia = tipo_dispositivo_ia
        self.estado_activo = estado_activo
        self.fecha_conexion = fecha_conexion if fecha_conexion else datetime.now()

    def to_dict(self):
        return {
            "id": self.id_dispositivos,
            "id_hogar": self.id_hogar,
            "name": self.alias,
            "id_dispositivo_iot": self.id_dispositivo_iot,
            "tipo_dispositivo_ia": self.tipo_dispositivo_ia,
            "connected": self.estado_activo,
            "icon": self._determinar_icono(),
            "fecha_conexion": self.fecha_conexion.isoformat() if self.fecha_conexion else None
        }

    def _determinar_icono(self):
        iconos = {
            'lampara': 'lightbulb',
            'luz': 'lightbulb',
            'tv': 'tv',
            'television': 'tv',
            'cafetera': 'coffee_maker',
            'cafe': 'coffee_maker',
            'enchufe': 'outlet',
            'tomacorriente': 'outlet',
            'aire': 'air',
            'ventilador': 'air',
        }
        
        if self.tipo_dispositivo_ia:
            tipo_lower = self.tipo_dispositivo_ia.lower()
            for key, icon in iconos.items():
                if key in tipo_lower:
                    return icon
        
        return 'outlet'  

    def __repr__(self):
        return f"<Dispositivo ID: {self.id_dispositivos}, Alias: {self.alias}, IoT ID: {self.id_dispositivo_iot}>"