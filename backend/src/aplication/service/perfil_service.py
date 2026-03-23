from typing import Dict, Any

from aplication.service.response_builder import success_response, error_response
from aplication.validators.perfil_validators import (
    validate_device_payload,
    validate_profile_payload,
)
from repositories.perfil_repository import PerfilRepository


def registrar_tomacorriente(data: Dict[str, Any], id_usuario: int, repo: PerfilRepository):
    error, payload = validate_device_payload(data)
    if error:
        return error_response(error, 400)

    device_id = payload["device_id"]
    alias = payload["alias"]

    if repo.device_exists(device_id):
        return error_response("Este dispositivo ya está registrado", 400)

    hogar = repo.get_hogar(id_usuario)
    if not hogar:
        return error_response("Debes crear un perfil de hogar primero", 400)

    dispositivo = repo.create_device(hogar.id_hogar, alias, device_id)
    if not dispositivo:
        return error_response("Error al registrar el dispositivo", 500)

    return success_response(
        {
            "message": "Dispositivo registrado exitosamente",
            "dispositivo": dispositivo.to_dict(),
        },
        201,
    )


def crear_perfil_hogar(data: Dict[str, Any], id_usuario: int, repo: PerfilRepository):
    error, payload = validate_profile_payload(data)
    if error:
        return error_response(error, 400)

    address = payload["address"]
    home_name = payload["home_name"]

    hogar = repo.save_hogar(id_usuario=id_usuario, direccion=address, nombre_hogar=home_name)
    if not hogar:
        return error_response("Error al guardar el perfil del hogar", 500)

    return success_response(
        {
            "message": "Perfil creado exitosamente",
            "hogar": hogar.to_dict(),
        },
        200,
    )


def actualizar_perfil_hogar(data: Dict[str, Any], id_usuario: int, repo: PerfilRepository, hogar_previo: Any):
    error, payload = validate_profile_payload(data)
    if error:
        return error_response(error, 400)

    address = payload["address"]
    home_name = payload["home_name"]

    hogar = repo.save_hogar(id_usuario=id_usuario, direccion=address, nombre_hogar=home_name)
    if not hogar:
        return error_response("Error al guardar el perfil del hogar", 500)

    return success_response(
        {
            "message": "Perfil actualizado exitosamente",
            "hogar": hogar.to_dict(),
        },
        200,
    )


def seleccionar_accion_perfil(data: Dict[str, Any], id_usuario: int, repo: PerfilRepository):
    """Decide si crear o actualizar según existencia previa."""
    hogar_previo = repo.get_hogar(id_usuario)
    if hogar_previo:
        return actualizar_perfil_hogar(data, id_usuario, repo, hogar_previo)
    return crear_perfil_hogar(data, id_usuario, repo)
