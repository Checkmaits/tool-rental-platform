from flask import Blueprint, request

import server.controllers.user_controller as controller

user_bp = Blueprint("users", __name__)


@user_bp.post("/")
def create():
    data = request.get_json()
    if not data:
        return {"error": {"status_code": 400, "message": "Request body must contain valid JSON"}}, 400

    return controller.create(data)
