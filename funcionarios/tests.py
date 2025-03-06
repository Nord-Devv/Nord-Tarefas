from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Funcionario

SECRET_KEY = "your_secret_key"


class FuncionarioAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.funcionario = Funcionario.objects.create(
            email_funcionario="test@example.com",
            senha_funcionario=make_password("password123"),  # Simulate hashed password
        )
        self.login_url = "/funcionario/funcionario/login_funcionario"
        self.logout_url = "/funcionario/funcionario/logout_funcionario"

    def test_login_funcionario_success(self):
        response = self.client.post(
            self.login_url,
            {
                "email_funcionario": "test@example.com",
                "senha_funcionario": "password123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_funcionario_invalid_credentials(self):
        response = self.client.post(
            self.login_url,
            {
                "email_funcionario": "test@example.com",
                "senha_funcionario": "wrongpassword",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Senha incorreta"})

    def test_login_funcionario_user_not_found(self):
        response = self.client.post(
            self.login_url,
            {
                "email_funcionario": "nonexistent@example.com",
                "senha_funcionario": "password123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Usuário não encontrado"})

    def test_logout_funcionario_success(self):
        session = self.client.session  # Get the test client session
        session["user_id"] = self.funcionario.id  # Set user as logged in
        session.save()  # Save session changes

        response = self.client.post(self.logout_url)  # Call the logout endpoint

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Logout realizado com sucesso"})

    def test_logout_funcionario_unauthenticated(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Usuário não autênticado"})
