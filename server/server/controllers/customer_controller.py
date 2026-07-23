from sqlalchemy.exc import IntegrityError

from server.extensions.db_extension import db
from server.models.address_model import Address
from server.models.customer_model import Customer


def create(data):
    errors = []

    customer = Customer()
    for field in ["first_name", "last_name", "company", "email", "phone_number", "password"]:
        try:
            setattr(customer, field, data.get(field))
        except ValueError as e:
            errors.append(str(e))

    address = Address()
    for field in ["address_line_1", "address_line_2", "city", "province", "postal_code"]:
        try:
            setattr(address, field, data.get(field))
        except ValueError as e:
            errors.append(str(e))

    if errors:
        return {"error": {"status_code": 400, "message": "Customer validation failed ❌", "errors": errors}}, 400

    try:
        customer.address = address
        db.session.add(customer)
        db.session.commit()
        return {"message": f"Customer created successfully (ID: {customer.id}) ✅"}, 201
    except IntegrityError:
        db.session.rollback()
        return {"error": {"status_code": 400, "message": "Customer validation failed ❌", "errors": ["A customer with that email address or phone number already exists ❌"]}}, 400
    except Exception:
        db.session.rollback()
        return {"error": {"status_code": 500, "message": "Internal server error ❌"}}, 500
