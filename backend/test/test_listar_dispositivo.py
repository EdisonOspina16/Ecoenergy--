
def listar_dispositivos(dispositivos, id_usuario):
    if not dispositivos:
        return []
    return [d for d in dispositivos if d["id_usuario"] == id_usuario]


# C1 – Usuario con dispositivos
def test_C1_con_dispositivos():
    datos = [
        {"id_usuario": 1, "nombre": "Lámpara", "consumo": 60, "estado": "encendido"},
        {"id_usuario": 1, "nombre": "Ventilador", "consumo": 100, "estado": "apagado"},
    ]
    resultado = listar_dispositivos(datos, 1)
    assert isinstance(resultado, list),        "C1 FALLO: resultado no es lista"
    assert len(resultado) == 2,                "C1 FALLO: esperaba 2 dispositivos"
    assert resultado[0]["nombre"] == "Lámpara","C1 FALLO: nombre incorrecto"
    print("C1 PASO ✓ – Lista de dispositivos retornada correctamente")


# C2 – Lista vacía (sin dispositivos en BD)
def test_C2_lista_vacia():
    resultado = listar_dispositivos([], 1)
    assert resultado == [], "C2 FALLO: debería retornar lista vacía"
    print("C2 PASO ✓ – Sin dispositivos retorna lista vacía")


# C3 – Usuario sin dispositivos registrados
def test_C3_usuario_sin_dispositivos():
    datos = [
        {"id_usuario": 2, "nombre": "Lámpara", "consumo": 60, "estado": "encendido"},
    ]
    resultado = listar_dispositivos(datos, 99)
    assert resultado == [], "C3 FALLO: usuario 99 no debería tener dispositivos"
    print("C3 PASO ✓ – Usuario sin dispositivos retorna lista vacía")


# C4 – Dispositivos nulos
def test_C4_datos_nulos():
    resultado = listar_dispositivos(None, 1)
    assert resultado == [], "C4 FALLO: datos None debería retornar lista vacía"
    print("C4 PASO ✓ – Datos None retorna lista vacía")


if __name__ == "__main__":
    print("\n══════════════════════════════════════")
    print("   PRUEBAS: LISTAR DISPOSITIVOS")
    print("══════════════════════════════════════")
    test_C1_con_dispositivos()
    test_C2_lista_vacia()
    test_C3_usuario_sin_dispositivos()
    test_C4_datos_nulos()
    print("\n✅ Todas las pruebas pasaron.\n")