from django.db import models

from funcionarios.models import Funcionario

from .choices import TarefaChoices


class Tarefa(models.Model):
    nome_tarefa = models.CharField(max_length=255)
    status_tarefa = models.CharField(
        max_length=255, choices=TarefaChoices.CHOICES, default=TarefaChoices.PENDENTE
    )
    atribuicao_tarefa = models.ForeignKey(
        Funcionario, on_delete=models.CASCADE, blank=True, null=True, default=None
    )
    descricao_tarefa = models.TextField(blank=True)
    prazo_inicial_tarefa = models.DateTimeField(
        auto_now_add=True, blank=True, null=True
    )
    prazo_final_tarefa = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.nome_tarefa
