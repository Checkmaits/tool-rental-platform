from sqlalchemy.exc import IntegrityError

from server.extensions.db_extension import db
from server.models.user_model import User


def create(data):
    errors = []

    user = User()
    for field in ["first_name", "last_name", "email", "password"]:
        try:
            setattr(user, field, data.get(field))
        except ValueError as e:
            errors.append(str(e))

    if errors:
        return {"error": {"status_code": 400, "message": "User validation failed ❌", "errors": errors}}, 400

    try:
        db.session.add(user)
        db.session.commit()
        return {"message": f"User created successfully (ID: {user.id}) ✅"}, 201
    except IntegrityError:
        db.session.rollback()
        return {"error": {"status_code": 400, "message": "User validation failed ❌", "errors": ["A user with email address already exists ❌"]}}, 400
    except Exception:
        db.session.rollback()
        return {"error": {"status_code": 500, "message": "Internal server error ❌"}}, 500
