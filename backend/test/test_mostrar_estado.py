
def mostrar_estado_dispositivo(dispositivos):
    if dispositivos is None:
        return {"success": False, "error": "error"}, 500
    return {"success": True, "dispositivos": dispositivos}, 200


# C1 – Con dispositivos
def test_C1_con_dispositivos():
    datos = [{"nombre": "Lámpara", "consumo": 60, "estado": "encendido", "watts": 75}]
    respuesta, status = mostrar_estado_dispositivo(datos)
    assert status == 200,                       "C1 FALLO: status debería ser 200"
    assert respuesta["success"] is True,        "C1 FALLO: success debería ser True"
    assert len(respuesta["dispositivos"]) == 1, "C1 FALLO: esperaba 1 dispositivo"
    assert respuesta["dispositivos"][0]["nombre"] == "Lámpara", "C1 FALLO: nombre incorrecto"
    print("C1 PASO ✓ – Estado retornado con dispositivos")


# C2 – Sin dispositivos
def test_C2_sin_dispositivos():
    respuesta, status = mostrar_estado_dispositivo([])
    assert status == 200,                   "C2 FALLO: status debería ser 200"
    assert respuesta["success"] is True,    "C2 FALLO: success debería ser True"
    assert respuesta["dispositivos"] == [], "C2 FALLO: lista debería estar vacía"
    print("C2 PASO ✓ – Sin dispositivos retorna lista vacía con success=True")


# C3 – Error / excepción
def test_C3_excepcion():
    respuesta, status = mostrar_estado_dispositivo(None)
    assert status == 500,                  "C3 FALLO: status debería ser 500"
    assert respuesta["success"] is False,  "C3 FALLO: success debería ser False"
    assert "error" in respuesta,           "C3 FALLO: debería contener clave 'error'"
    print("C3 PASO ✓ – Error retorna 500 con success=False")


if __name__ == "__main__":
    print("\n══════════════════════════════════════")
    print("   PRUEBAS: MOSTRAR ESTADO DISPOSITIVO")
    print("══════════════════════════════════════")
    test_C1_con_dispositivos()
    test_C2_sin_dispositivos()
    test_C3_excepcion()
    print("\n✅ Todas las pruebas pasaron.\n")