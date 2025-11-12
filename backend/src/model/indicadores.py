from datetime import datetime

class Indicadores:
    def __init__(self, id_indicador=None, usuario_id=None, energia_ahorrada_kwh=0, 
                 reduccion_co2_kg=0, arboles_salvados=0, ahorro_economico=0, 
                 periodo=None, fecha_creacion=None):
        self.id_indicador = id_indicador
        self.usuario_id = usuario_id
        
        self.energia_ahorrada_kwh = max(0, energia_ahorrada_kwh)
        self.reduccion_co2_kg = max(0, reduccion_co2_kg)
        self.arboles_salvados = max(0, arboles_salvados)
        self.ahorro_economico = max(0, ahorro_economico)
        
        self.periodo = periodo if periodo else datetime.now().date()
        self.fecha_creacion = fecha_creacion if fecha_creacion else datetime.now()

    def to_dict(self):
        return {
            "id_indicador": self.id_indicador,
            "usuario_id": self.usuario_id,
            "energia_ahorrada_kwh": float(self.energia_ahorrada_kwh),
            "reduccion_co2_kg": float(self.reduccion_co2_kg),
            "arboles_salvados": float(self.arboles_salvados),
            "ahorro_economico": float(self.ahorro_economico),
            "periodo": self.periodo.isoformat() if self.periodo else None,
            "fecha_creacion": self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_creacion else None
        }

    @staticmethod
    def from_dict(data):
        periodo = None
        if data.get('periodo'):
            if isinstance(data['periodo'], str):
                periodo = datetime.fromisoformat(data['periodo']).date()
            else:
                periodo = data['periodo']
        
        fecha_creacion = None
        if data.get('fecha_creacion'):
            if isinstance(data['fecha_creacion'], str):
                fecha_creacion = datetime.strptime(data['fecha_creacion'], '%Y-%m-%d %H:%M:%S')
            else:
                fecha_creacion = data['fecha_creacion']
        
        return Indicadores(
            id_indicador=data.get('id_indicador'),
            usuario_id=data.get('usuario_id'),
            energia_ahorrada_kwh=data.get('energia_ahorrada_kwh', 0),
            reduccion_co2_kg=data.get('reduccion_co2_kg', 0),
            arboles_salvados=data.get('arboles_salvados', 0),
            ahorro_economico=data.get('ahorro_economico', 0),
            periodo=periodo,
            fecha_creacion=fecha_creacion
        )

    def __repr__(self):
        return (f"<Indicadores ID: {self.id_indicador}, Usuario: {self.usuario_id}, "
                f"Energía: {self.energia_ahorrada_kwh}kWh, Árboles: {self.arboles_salvados}, "
                f"Ahorro: ${self.ahorro_economico}>")

    def __str__(self):
        """Representación legible para el usuario"""
        return (f"Indicadores del usuario {self.usuario_id}:\n"
                f"  - Energía ahorrada: {self.energia_ahorrada_kwh} kWh\n"
                f"  - CO2 reducido: {self.reduccion_co2_kg} kg\n"
                f"  - Árboles salvados: {self.arboles_salvados}\n"
                f"  - Ahorro económico: ${self.ahorro_economico:,.2f}\n"
                f"  - Período: {self.periodo}")