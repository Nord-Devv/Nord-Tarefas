from datetime import datetime

from django.test import TestCase
from django.utils.timezone import make_aware

from funcionarios.models import Funcionario
from tarefas.models import Tarefa


class TarefaAPITestCase(TestCase):
    def setUp(self):
        self.funcionario = Funcionario.objects.create(
            nome_funcionario="Teste Funcionario"
        )
        self.tarefa = Tarefa.objects.create(
            nome_tarefa="Tarefa Teste",
            status_tarefa="Pendente",
            atribuicao_tarefa=self.funcionario,
            descricao_tarefa="Teste",
            prazo_inicial_tarefa=make_aware(datetime(2024, 2, 1, 8, 0, 0)),
            prazo_final_tarefa=make_aware(datetime(2024, 2, 2, 18, 0, 0)),
        )

        self.tarefa = Tarefa.objects.create(
            nome_tarefa="Tarefa Teste",
            status_tarefa="Pendente",
            atribuicao_tarefa=self.funcionario,
            descricao_tarefa="Descrição da tarefa de teste",
            prazo_inicial_tarefa=datetime(2024, 1, 1, 10, 0, 0),
            prazo_final_tarefa=datetime(2024, 1, 2, 18, 0, 0),
        )

        self.listar_url = "/tarefa/tarefa/listar_tarefas"
        self.adicionar_url = "/tarefa/tarefa/adicionar_tarefas"
        self.remover_url = "/tarefa/tarefa/remover_tarefa"
        self.alterar_url = "/tarefa/tarefa/alterar_tarefa"

    def test_listar_tarefas(self):
        response = self.client.get(self.listar_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["nome_tarefa"], "Tarefa Teste")

    def test_adicionar_tarefa(self):
        payload = {
            "nome_tarefa": "Nova Tarefa",
            "status_tarefa": "Em andamento",
            "descricao_tarefa": "Descrição de nova tarefa",
            "atribuicao_tarefa": self.funcionario.id,
            "prazo_inicial_tarefa": "2024-02-01T08:00:00Z",
            "prazo_final_tarefa": "2024-02-02T18:00:00Z",
        }
        response = self.client.post(self.adicionar_url, data=payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nome_tarefa"], "Nova Tarefa")

    def test_remover_tarefa(self):
        response = self.client.delete(self.remover_url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tarefa.objects.filter(nome_tarefa="Tarefa Teste").exists())

    def test_alterar_tarefa(self):
        payload = {
            "nome_tarefa": "Tarefa Modificada",
            "status_tarefa": "Concluída",
            "descricao_tarefa": "Descrição alterada",
            "atribuicao_tarefa": self.funcionario.id,
            "prazo_inicial_tarefa": "2024-03-01T08:00:00Z",
            "prazo_final_tarefa": "2024-03-02T18:00:00Z",
        }
        response = self.client.put(self.alterar_url, data=payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nome_tarefa"], "Tarefa Modificada")
