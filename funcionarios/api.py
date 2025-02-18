from datetime import datetime, timedelta

import jwt
import pytz
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from ninja import NinjaAPI
from ninja.errors import HttpError

from .schemas import LoginFuncionarioSchema

SECRET_KEY = "your_secret_key"

api_funcionario = NinjaAPI(urls_namespace="funcionarios")


class FuncionarioAPI:
    @staticmethod
    @api_funcionario.post("/funcionario/login")
    def login_funcionario(request, data: LoginFuncionarioSchema):
        try:
            # Get the user's timezone from the request (e.g., in headers or body)
            user_timezone = request.headers.get(
                "Timezone", "UTC"
            )  # Default to UTC if not provided

            # Fetch the funcionario
            funcionario = funcionario.objects.filter(
                email_funcionario=data.email_funcionario
            ).first()

            if not funcionario:
                return JsonResponse({"error": "Usuário não encontrado"}, status=400)

            if not check_password(
                data.senha_funcionario, funcionario.senha_funcionario
            ):
                return JsonResponse({"error": "Senha incorreta"}, status=400)

            # Get the current time in UTC
            now_utc = datetime.now(pytz.utc)

            # Convert the current time to the user's timezone
            user_tz = pytz.timezone(user_timezone)
            now_user_tz = now_utc.astimezone(user_tz)

            # Calculate the expiration time in the user's timezone
            expiration_time = now_user_tz + timedelta(days=1)

            # Encode the token with the expiration time in UTC (JWT expects UTC)
            expiration_time_utc = expiration_time.astimezone(pytz.utc)
            token = jwt.encode(
                {
                    "email_funcionario": funcionario.email_funcionario,
                    "exp": expiration_time_utc,
                },
                SECRET_KEY,
                algorithm="HS256",
            )

            return JsonResponse({"message": "Login bem-sucedido", "token": token})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    @api_funcionario.post("/funcionario/logout")
    def logout_funcionario(request):
        if "user_id" in request.session:
            logout(request)
            return {"message": "Logout realizado com sucesso"}
        else:
            raise HttpError(401, "Usuário não autênticado")
