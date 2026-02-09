
from src.model.subscriber import create_subscriber
from src.controller.controladorEmail import send_welcome_email

def subscribe_user(email):
    if not email:
        return False, "Correo obligatorio"

    created = create_subscriber(email)

    if not created:
        return False, "Correo ya registrado"

    send_welcome_email(email)
    return True, "Correo registrado y enviado"
