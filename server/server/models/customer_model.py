import re
from datetime import datetime

import phonenumbers
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash

from server.extensions.db_extension import db

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]).{8,64}$")


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(100))
    email = db.Column(db.String(254), nullable=False, unique=True, index=True)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id", ondelete="CASCADE"), nullable=False, unique=True)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    address = db.relationship("Address", cascade="all, delete-orphan", uselist=False, single_parent=True, foreign_keys=[address_id])

    @validates("first_name", "last_name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Customer '{key}' is a required field")

        name = value.strip()
        if not 2 <= len(name) <= 50:
            raise ValueError("Customer '{key}' must be between 2 and 50 characters long")

        return name

    @validates("company")
    def validate_company(self, key, value):
        if value is None:
            return None

        if not isinstance(value, str):
            raise ValueError("Customer 'company' must be a valid string")

        company = value.strip()
        if not company:
            return None
        if len(company) > 100:
            raise ValueError("Customer 'company' cannot exceed 100 characters")

        return company

    @validates("email")
    def validate_email(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Customer 'email' is a required field")

        email = value.lower().strip()
        if not 6 <= len(email) <= 254:
            raise ValueError("Customer 'email' must be between 6 and 254 characters long")
        if not EMAIL_REGEX.fullmatch(email):
            raise ValueError("Customer 'email' must be a valid email address")

        return email

    @validates("phone_number")
    def validate_phone_number(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Customer 'phone_number' is a required field")

        try:
            phone_number = phonenumbers.parse(value.strip(), "CA")
            if not phonenumbers.is_valid_number(phone_number):
                raise ValueError("Customer 'phone_number' must be a valid Canadian phone number")

            return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise ValueError("Customer 'phone_number' must be a valid Canadian phone number")

    @property
    def password(self):
        raise AttributeError("Customer 'password' is a write-only field!")

    @password.setter
    def password(self, plaintext_password):
        if not isinstance(plaintext_password, str) or not plaintext_password:
            raise ValueError("Customer 'password' is a required field")
        if not PASSWORD_REGEX.fullmatch(plaintext_password):
            raise ValueError("Customer 'password' must be between 8 and 64 characters long and contain an uppercase letter, a lowercase letter, a number, and a special character")

        self.password_hash = generate_password_hash(plaintext_password, method="scrypt")

    def verify_password(self, plaintext_password):
        return check_password_hash(self.password_hash, plaintext_password)
