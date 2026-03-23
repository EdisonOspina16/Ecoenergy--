from src.repositories.consumo_repository import (
    obtener_dispositivos_con_ultimo_consumo,
    obtener_dispositivos_por_usuario,
    obtener_recomendacion_diaria,
    guardar_recomendacion_diaria,
)
from src.infrastructure.ia.gemini_service import (
    llamar_recomendacion,
    llamar_ahorro_estimado,
)
from src.database import obtener_conexion
from src.repositories.usuario_repository import UsuarioRepository


def _obtener_hogar(id_usuario: int):
    """Instancia el repo con conexión y retorna el hogar del usuario."""
    conn = obtener_conexion()
    repo = UsuarioRepository(conn)
    return repo.obtener_hogar_por_usuario(id_usuario)


def _construir_item_recomendacion(dispositivo: str, consumo_watts: float) -> dict:
    """
    Genera y estructura la recomendación de un dispositivo.
    """
    texto = llamar_recomendacion(consumo_watts, dispositivo)
    es_alerta = any(
        p in texto.lower() for p in ["⚠️", "pico", "anómalo", "inusual", "alerta"]
    )
    return {
        "recomendacion": texto,
        "esAlerta": es_alerta,
        "dispositivo": dispositivo,
    }


def procesar_recomendacion(consumo_watts: float, dispositivo: str) -> dict:
    """
    Genera la recomendación para un dispositivo puntual.
    Usado por el endpoint POST /recomendacion.
    """
    texto = llamar_recomendacion(consumo_watts, dispositivo)
    es_alerta = any(
        p in texto.lower() for p in ["⚠️", "pico", "anómalo", "inusual", "alerta"]
    )
    return {
        "recomendacion": texto,
        "esAlerta": es_alerta,
        "dispositivo": dispositivo,
    }


def procesar_ahorro_estimado() -> dict:
    """
    Obtiene todos los dispositivos y genera el ahorro estimado.
    Usado por el endpoint GET /ahorro-estimado.
    """
    dispositivos = obtener_dispositivos_con_ultimo_consumo()
    if not dispositivos:
        raise ValueError("No hay dispositivos registrados para calcular el ahorro.")
    return llamar_ahorro_estimado(dispositivos)


def obtener_recomendacion_diaria_hogar_por_usuario(id_usuario: int) -> dict:
    hogar = _obtener_hogar(id_usuario)
    if not hogar:
        return {
            "encontrado": False,
            "recomendaciones": [],
            "ahorro_financiero": None,
            "impacto_ambiental": None,
            "indicador_didactico": None,
        }
    registro = obtener_recomendacion_diaria(hogar.id_hogar)
    if registro:
        return {"encontrado": True, **registro}
    return {
        "encontrado": True,
        "recomendaciones": [],
        "ahorro_financiero": None,
        "impacto_ambiental": None,
        "indicador_didactico": None,
    }


def generar_y_guardar_recomendacion_diaria(id_usuario: int) -> dict:
    hogar = _obtener_hogar(id_usuario)
    if not hogar:
        raise ValueError("No tienes un hogar registrado.")

    registro_existente = obtener_recomendacion_diaria(hogar.id_hogar)
    if registro_existente:
        return {"generada": True, **registro_existente}

    dispositivos = obtener_dispositivos_por_usuario(id_usuario)
    if not dispositivos:
        raise ValueError("No hay dispositivos registrados para generar la recomendación.")

    recomendaciones = [
        _construir_item_recomendacion(d["nombre"], d["consumo_watts"])
        for d in dispositivos
    ]
    ahorro = llamar_ahorro_estimado(dispositivos)
    guardar_recomendacion_diaria(hogar.id_hogar, recomendaciones, ahorro)

    return {
        "generada": True,
        "recomendaciones": recomendaciones,
        "ahorro_financiero": ahorro.get("ahorro_financiero"),
        "impacto_ambiental": ahorro.get("impacto_ambiental"),
        "indicador_didactico": ahorro.get("indicador_didactico"),
    }