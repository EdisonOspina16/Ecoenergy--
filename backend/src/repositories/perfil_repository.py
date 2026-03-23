from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class PerfilRepository:
    obtener_hogar: Callable[[int], Any]
    crear_o_actualizar_hogar: Callable[[int, str, str], Any]
    verificar_dispositivo_existe: Callable[[str], bool]
    crear_dispositivo: Callable[[int, str, str], Any]

    def get_hogar(self, id_usuario: int):
        return self.obtener_hogar(id_usuario)

    def save_hogar(self, id_usuario: int, direccion: str, nombre_hogar: str):
        return self.crear_o_actualizar_hogar(id_usuario=id_usuario, direccion=direccion, nombre_hogar=nombre_hogar)

    def device_exists(self, device_id: str) -> bool:
        return self.verificar_dispositivo_existe(device_id)

    def create_device(self, id_hogar: int, alias: str, device_id: str):
        return self.crear_dispositivo(id_hogar=id_hogar, alias=alias, id_dispositivo_iot=device_id)
