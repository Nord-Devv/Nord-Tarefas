# Generated by Django 5.1.6 on 2025-02-18 19:01

import storages.backends.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Funcionario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome_funcionario", models.CharField(max_length=255)),
                (
                    "foto_funcionario",
                    models.ImageField(
                        storage=storages.backends.s3.S3Storage(),
                        upload_to="funcionarios/",
                    ),
                ),
                ("sobrenome_funcionario", models.CharField(max_length=255)),
                ("email_funcionario", models.EmailField(max_length=254)),
                ("senha_funcionario", models.CharField(max_length=255)),
                ("descricao_funcionario", models.TextField(blank=True)),
            ],
        ),
    ]
