from django.db import models


class Funcionario(models.Model):
    nome_funcionario = models.CharField(max_length=255)
    sobrenome_funcionario = models.CharField(max_length=255)
    email_funcionario = models.EmailField()
    senha_funcionario = models.CharField(max_length=255)
    descricao_funcionario = models.TextField(blank=True)
