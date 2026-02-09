from flask import Blueprint, request, jsonify
from controller.controladorEmail import send_welcome_email

email_bp = Blueprint("email", __name__)

@email_bp.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email requerido"}), 400

    send_welcome_email(email)
    return jsonify({"message": "Correo enviado correctamente"}), 200
