from flask import jsonify


def success_response(payload: dict, status_code: int = 200):
    return jsonify({"success": True, **payload}), status_code


def error_response(message: str, status_code: int = 400):
    return jsonify({"success": False, "error": message}), status_code
