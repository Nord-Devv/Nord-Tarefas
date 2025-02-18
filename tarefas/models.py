from django.db import models

from funcionarios.models import Funcionario

class Tarefa(models.Model):
    nome_tarefa = models.CharField(max_length=255)
    atribuicao_tarefa = models.ForeignKey(
        Funcionario, on_delete=models.CASCADE,
        blank=True, null=True, default=None
    )
    descricao_tarefa = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    