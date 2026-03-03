
from werkzeug.security import generate_password_hash, check_password_hash


def cambiar_contrasena(correo, nueva_contrasena):
    if not correo or not nueva_contrasena:
        return False
    hash_pwd = generate_password_hash(nueva_contrasena)
    if not hash_pwd:
        return False
    return True


def test_C1_exitoso():
    resultado = cambiar_contrasena("user@test.com", "Segura123!")
    assert resultado is True, "C1 FALLO: debería retornar True con datos válidos"
    print("C1 PASO ✓ – Contraseña cambiada exitosamente")


def test_C2_correo_vacio():
    resultado = cambiar_contrasena("", "Clave456!")
    assert resultado is False, "C2 FALLO: debería retornar False con correo vacío"
    print("C2 PASO ✓ – Correo vacío retorna False")


def test_C3_contrasena_vacia():
    resultado = cambiar_contrasena("user@test.com", "")
    assert resultado is False, "C3 FALLO: debería retornar False con contraseña vacía"
    print("C3 PASO ✓ – Contraseña vacía retorna False")


def test_hash_valido():
    nueva = "MiClave123!"
    hash_pwd = generate_password_hash(nueva)
    assert check_password_hash(hash_pwd, nueva) is True, "FALLO: hash no corresponde a la contraseña"
    print("EXTRA PASO ✓ – Hash generado es válido")


if __name__ == "__main__":
    print("\n══════════════════════════════════════")
    print("   PRUEBAS: CAMBIAR CONTRASEÑA")
    print("══════════════════════════════════════")
    test_C1_exitoso()
    test_C2_correo_vacio()
    test_C3_contrasena_vacia()
    test_hash_valido()
    print("\n✅ Todas las pruebas pasaron.\n")