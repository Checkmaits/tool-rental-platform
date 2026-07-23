import re

from sqlalchemy.orm import validates

from server.extensions.db_extension import db

PROVINCE_REGEX = re.compile(r"^(AB|BC|MB|NB|NL|NS|NT|NU|ON|PE|QC|SK|YT)$")
POSTAL_CODE_REGEX = re.compile(r"^[A-Z]\d[A-Z]\d[A-Z]\d$")


class Address(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_line_1 = db.Column(db.String(100), nullable=False)
    address_line_2 = db.Column(db.String(100))
    city = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(2), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)

    @validates("address_line_1")
    def validate_address_line_1(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Address 'address_line_1' is a required field")

        address_line_1 = value.strip()
        if not 3 <= len(address_line_1) <= 100:
            raise ValueError("Address 'address_line_1' must be between 3 and 100 characters long")

        return address_line_1

    @validates("address_line_2")
    def validate_address_line_2(self, key, value):
        if value is None:
            return None

        if not isinstance(value, str):
            raise ValueError("Address 'address_line_2' must be a valid string")

        address_line_2 = value.strip()
        if not address_line_2:
            return None
        if len(address_line_2) > 100:
            raise ValueError("Address 'address_line_2' cannot exceed 100 characters")

        return address_line_2

    @validates("city")
    def validate_city(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Address 'city' is a required field")

        city = value.strip()
        if not 3 <= len(city) <= 100:
            raise ValueError("Address 'city' must be between 3 and 100 characters long")

        return city

    @validates("province")
    def validate_province(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Address 'province' is a required field")

        province = value.upper().strip()
        if not PROVINCE_REGEX.fullmatch(province):
            raise ValueError("Address 'province' must be a valid Canadian province or territory code")

        return province

    @validates("postal_code")
    def validate_postal_code(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Address 'postal_code' is a required field")

        postal_code = value.replace(" ", "").replace("-", "").upper()
        if not POSTAL_CODE_REGEX.fullmatch(postal_code):
            raise ValueError("Address 'postal_code' must be a valid Canadian postal code")

        return postal_code
