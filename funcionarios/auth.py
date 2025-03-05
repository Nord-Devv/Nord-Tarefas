from datetime import datetime

import pytz
from jwt import ExpiredSignatureError, InvalidTokenError, decode
from ninja.security import HttpBearer

SECRET_KEY = "your_secret_key"


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = decode(token, SECRET_KEY, algorithms=["HS256"])
            exp = payload.get("exp")
            if exp and datetime.now(pytz.utc) > datetime.fromtimestamp(
                exp, tz=pytz.utc
            ):
                raise InvalidTokenError("Token has expired")
            return payload
        except ExpiredSignatureError:
            raise InvalidTokenError("Token has expired")
        except InvalidTokenError:
            raise InvalidTokenError("Invalid token")
