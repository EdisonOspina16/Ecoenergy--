from typing import Any, Dict, Tuple


def is_device_payload(data: Dict[str, Any]) -> bool:
    return "deviceId" in data and "nickname" in data


def is_profile_payload(data: Dict[str, Any]) -> bool:
    return "address" in data and "nombre_hogar" in data


def validate_device_payload(data: Dict[str, Any]) -> Tuple[str | None, dict | None]:
    if not data:
        return "Datos requeridos para registrar dispositivo", None

    device_id = data.get("deviceId", "")
    alias = data.get("nickname", "")

    if not device_id or not alias:
        return "ID del dispositivo y alias son requeridos", None

    return None, {"device_id": device_id, "alias": alias}


def validate_profile_payload(data: Dict[str, Any]) -> Tuple[str | None, dict | None]:
    if not data:
        return "La dirección y el nombre del hogar son requeridos", None

    address = data.get("address", "")
    home_name = data.get("nombre_hogar", "")

    if not address or not home_name:
        return "La dirección y el nombre del hogar son requeridos", None

    return None, {"address": address, "home_name": home_name}
