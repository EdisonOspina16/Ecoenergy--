
def registrar_suscripcion(email, create_subscriber, send_email):
    if not email:
        return False, "Correo obligatorio"
    creado = create_subscriber(email)
    if not creado:
        return False, "Correo ya registrado"
    send_email(email)
    return True, "Correo registrado y enviado"


# C1 – Email válido, suscriptor creado y email enviado
def test_C1_exitoso():
    emails_enviados = []

    def create_subscriber(email): return True
    def send_email(email): emails_enviados.append(email)

    resultado, mensaje = registrar_suscripcion("user@correo.com", create_subscriber, send_email)

    assert resultado is True,                        "C1 FALLO: debería retornar True"
    assert mensaje == "Correo registrado y enviado", "C1 FALLO: mensaje incorrecto"
    assert "user@correo.com" in emails_enviados,     "C1 FALLO: email no fue enviado"
    print("C1 PASO ✓ – Suscripción registrada y correo enviado")


# C2 – Email vacío
def test_C2_email_vacio():
    def create_subscriber(email): return True
    def send_email(email): pass

    resultado, mensaje = registrar_suscripcion("", create_subscriber, send_email)

    assert resultado is False,              "C2 FALLO: debería retornar False"
    assert mensaje == "Correo obligatorio", "C2 FALLO: mensaje incorrecto"
    print("C2 PASO ✓ – Email vacío retorna False con mensaje obligatorio")


# C3 – Correo ya registrado
def test_C3_correo_ya_registrado():
    def create_subscriber(email): return False
    def send_email(email): pass

    resultado, mensaje = registrar_suscripcion("user@correo.com", create_subscriber, send_email)

    assert resultado is False,                 "C3 FALLO: debería retornar False"
    assert mensaje == "Correo ya registrado",  "C3 FALLO: mensaje incorrecto"
    print("C3 PASO ✓ – Correo ya registrado retorna False")


if __name__ == "__main__":
    print("\n══════════════════════════════════════")
    print("   PRUEBAS: REGISTRAR SUSCRIPCIÓN CORREO")
    print("══════════════════════════════════════")
    test_C1_exitoso()
    test_C2_email_vacio()
    test_C3_correo_ya_registrado()
    print("\n✅ Todas las pruebas pasaron.\n")