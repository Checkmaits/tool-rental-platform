from flask import Blueprint, request

import server.controllers.customer_controller as controller

customer_bp = Blueprint("customers", __name__)


@customer_bp.post("/")
def create():
    data = request.get_json()
    if not data:
        return {"error": {"status_code": 400, "message": "Request body must contain valid JSON"}}, 400

    return controller.create(data)
