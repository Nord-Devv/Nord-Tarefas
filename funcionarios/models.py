from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


class Funcionario(models.Model):
    nome_funcionario = models.CharField(max_length=255)
    foto_funcionario = models.ImageField(upload_to='funcionarios/', storage=S3Boto3Storage())
    sobrenome_funcionario = models.CharField(max_length=255)
    email_funcionario = models.EmailField()
    senha_funcionario = models.CharField(max_length=255)
    descricao_funcionario = models.TextField(blank=True)
