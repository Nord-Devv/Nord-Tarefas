from datetime import datetime, timedelta

import jwt
import pytz
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from ninja import NinjaAPI
from ninja.errors import HttpError

from .auth import JWTAuth
from .models import Funcionario
from .schemas import LoginFuncionarioSchema

SECRET_KEY = "your_secret_key"

api_funcionario = NinjaAPI(urls_namespace="funcionarios", auth=JWTAuth())


class FuncionarioAPI:
    @staticmethod
    @api_funcionario.post("/login_funcionario", auth=None)
    def login_funcionario(request, data: LoginFuncionarioSchema):
        try:
            user_timezone = request.headers.get("Timezone", "UTC")

            funcionario = Funcionario.objects.filter(
                email_funcionario=data.email_funcionario
            ).first()

            if not funcionario:
                return JsonResponse({"error": "Usuário não encontrado"}, status=400)

            if not check_password(
                data.senha_funcionario, funcionario.senha_funcionario
            ):
                return JsonResponse({"error": "Senha incorreta"}, status=400)

            now_utc = datetime.now(pytz.utc)
            user_tz = pytz.timezone(user_timezone)
            now_user_tz = now_utc.astimezone(user_tz)
            expiration_time = now_user_tz + timedelta(hours=1)
            expiration_time_utc = expiration_time.astimezone(pytz.utc)

            # Generate JWT token
            token = jwt.encode(
                {
                    "email_funcionario": funcionario.email_funcionario,
                    "exp": expiration_time_utc,
                },
                SECRET_KEY,
                algorithm="HS256",
            )

            print("Generated token:", token)  # Debugging
            return JsonResponse({"message": "Login bem-sucedido", "token": token})

        except Exception as e:
            print("Login error:", str(e))  # Debugging
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    @api_funcionario.post("/logout_funcionario", auth=None)  # Allow access without token
    def logout_funcionario(request):
        try:
            # Optionally, blacklist the token here
            return {"message": "Logout realizado com sucesso"}
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)