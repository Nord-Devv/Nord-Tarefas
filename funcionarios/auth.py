from datetime import datetime

import jwt
from django.conf import settings
from ninja.security import HttpBearer

SECRET_KEY = "your_secret_key"


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            exp = payload.get("exp")
            if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
                return None  # Token expired

            return payload  # Valid token
        except jwt.ExpiredSignatureError:
            return None  # Token expired
        except jwt.InvalidTokenError:
            return None  # Invalid token
