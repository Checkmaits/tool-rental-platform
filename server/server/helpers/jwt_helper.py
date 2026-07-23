import os
from datetime import datetime, timedelta, timezone

import jwt


def create_jwt(payload, expiry):
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {**payload, "iat": now, "exp": now + timedelta(hours=expiry)},
        key=os.getenv("JWT_SECRET"),
        algorithm="HS256",
    )
