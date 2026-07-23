from flask import Blueprint, request

import server.controllers.admin_auth_controller as controller

admin_auth_bp = Blueprint("admin_auth", __name__)


@admin_auth_bp.post("/login")
def login():
    data = request.get_json()
    if not data:
        return {"error": {"status_code": 400, "message": "Request body must contain valid JSON"}}, 400

    return controller.login(data)


@admin_auth_bp.post("/logout")
def logout():
    return controller.logout()
