
def crear_perfil(conn_valida, fila):
    if not conn_valida:
        return None
    if not fila:
        return None
    return {"id_hogar": fila["id_hogar"], "nombre": fila["nombre"]}


# C1 – Flujo exitoso: conn válida y fila válida
def test_C1_exitoso():
    resultado = crear_perfil(True, {"id_hogar": 1, "nombre": "Hogar Principal"})
    assert resultado is not None,                      "C1 FALLO: debería retornar objeto"
    assert resultado["nombre"] == "Hogar Principal",   "C1 FALLO: nombre incorrecto"
    assert resultado["id_hogar"] == 1,                 "C1 FALLO: id_hogar incorrecto"
    print("C1 PASO ✓ – Perfil creado y retornado correctamente")


# C2 – Fila vacía/None
def test_C2_fila_vacia():
    resultado = crear_perfil(True, None)
    assert resultado is None, "C2 FALLO: debería retornar None con fila vacía"
    print("C2 PASO ✓ – Fila None retorna None")


# C3 – Sin conexión
def test_C3_sin_conexion():
    resultado = crear_perfil(False, {"id_hogar": 1, "nombre": "Hogar"})
    assert resultado is None, "C3 FALLO: debería retornar None sin conexión"
    print("C3 PASO ✓ – Sin conexión retorna None")


# C4 – Excepción simulada (conn y fila inválidas)
def test_C4_excepcion():
    resultado = crear_perfil(False, None)
    assert resultado is None, "C4 FALLO: debería retornar None en caso de error"
    print("C4 PASO ✓ – Error retorna None")


if __name__ == "__main__":
    print("\n══════════════════════════════════════")
    print("   PRUEBAS: CREAR PERFIL")
    print("══════════════════════════════════════")
    test_C1_exitoso()
    test_C2_fila_vacia()
    test_C3_sin_conexion()
    test_C4_excepcion()
    print("\n✅ Todas las pruebas pasaron.\n")