from ninja.security import HttpBearer
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime
import pytz


SECRET_KEY = "your_secret_key"

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            # Decode the token
            payload = decode(token, SECRET_KEY, algorithms=["HS256"])
            # Check if the token has expired
            exp = payload.get("exp")
            if exp and datetime.now(pytz.utc) > datetime.fromtimestamp(exp, tz=pytz.utc):
                raise InvalidTokenError("Token has expired")
            return payload  # Return the payload if valid
        except ExpiredSignatureError:
            raise InvalidTokenError("Token has expired")
        except InvalidTokenError:
            raise InvalidTokenError("Invalid token")