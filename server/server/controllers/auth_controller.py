from flask import make_response
from sqlalchemy import select

from server.extensions.db_extension import db
from server.helpers.jwt_helper import create_jwt
from server.models.customer_model import Customer


def login(data):
    email = data.get("email")
    password = data.get("password")

    missing_fields = []
    if not isinstance(email, str) or not email.strip():
        missing_fields.append("email")
    if not isinstance(password, str) or not password:
        missing_fields.append("password")
    if missing_fields:
        return {"error": {"status_code": 400, "message": f"Missing required fields: {','.join(missing_fields)} ❌"}}, 400

    try:
        stmt = select(Customer).where(Customer.email == email.lower().strip())
        result = db.session.execute(stmt)
        customer = result.scalar_one_or_none()
        if not customer or not customer.verify_password(password):
            return {"error": {"status_code": 401, "message": "Invalid email or password ❌"}}, 401

        response = make_response({"message": f"Customer logged in successfully (ID: {customer.id}) ✅"})
        response.status_code = 200
        response.set_cookie("c_token", create_jwt({"id": customer.id}, 24), httponly=True, secure=False, samesite="lax", max_age=(60 * 60 * 24))
        return response
    except Exception:
        return {"error": {"status_code": 500, "message": "Internal server error ❌"}}, 500


def logout():
    response = make_response({"message": "Customer logged out successfully ✅"})
    response.status_code = 200
    response.delete_cookie("c_token")
    return response
