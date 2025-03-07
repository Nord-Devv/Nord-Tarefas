from datetime import datetime, timedelta

import jwt
import pytz
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from funcionarios.models import Funcionario

from .models import DeletedTarefa, Tarefa


class TarefaAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.funcionario = Funcionario.objects.create(
            email_funcionario="test@example.com",
            senha_funcionario="dummy_password",  # Use make_password in real scenarios
        )
        self.tarefa = Tarefa.objects.create(
            nome_tarefa="Test Task",
            descricao_tarefa="Test Description",
            status_tarefa="Pendente",
            prazo_inicial_tarefa=timezone.make_aware(timezone.datetime(2023, 1, 1)),
            prazo_final_tarefa=timezone.make_aware(timezone.datetime(2023, 1, 10)),
            atribuicao_tarefa=self.funcionario,
        )

        expiration_time_utc = datetime.now(pytz.utc) + timedelta(hours=1)
        self.token = jwt.encode(
            {
                "email_funcionario": self.funcionario.email_funcionario,
                "exp": expiration_time_utc,
            },
            "your_secret_key",
            algorithm="HS256",
        )

    def test_listar_tarefas(self):
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}
        response = self.client.get(reverse("tarefas:listar_tarefas"), **headers)
        self.assertEqual(response.status_code, 200)

    def test_remover_tarefa(self):
        # Authenticate the request
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}

        # Make the request
        response = self.client.delete(
            reverse("tarefas:remover_tarefa", args=["Test Task"]), **headers
        )

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        deleted_tarefa = DeletedTarefa.objects.filter(nome_tarefa="Test Task").first()
        self.assertIsNotNone(deleted_tarefa)

        # Check if the task was deleted from Tarefa
        tarefa_exists = Tarefa.objects.filter(nome_tarefa="Test Task").exists()
        self.assertFalse(tarefa_exists)
