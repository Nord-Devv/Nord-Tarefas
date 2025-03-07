from datetime import datetime

import pytz
from django.core.cache import cache
from jwt import ExpiredSignatureError, InvalidTokenError, decode
from ninja.security import HttpBearer

SECRET_KEY = "your_secret_key"


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            # Check if the token is invalidated
            if cache.get(token) == "invalid":
                raise InvalidTokenError("Token inválido")

            payload = decode(token, SECRET_KEY, algorithms=["HS256"])
            exp = payload.get("exp")
            if exp and datetime.now(pytz.utc) > datetime.fromtimestamp(
                exp, tz=pytz.utc
            ):
                raise InvalidTokenError("Token expirado")
            return payload
        except ExpiredSignatureError:
            raise InvalidTokenError("Token expirado")
        except InvalidTokenError:
            raise InvalidTokenError("Token inválido")
