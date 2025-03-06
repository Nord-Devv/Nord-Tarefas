# Generated by Django 5.1.6 on 2025-03-06 00:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0002_alter_funcionario_foto_funcionario'),
        ('tarefas', '0004_tarefa_deletada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarefa',
            name='deletada',
        ),
        migrations.CreateModel(
            name='DeletedTarefa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_tarefa', models.CharField(max_length=255)),
                ('descricao_tarefa', models.TextField()),
                ('status_tarefa', models.CharField(choices=[('A fazer', 'A fazer'), ('Em andamento', 'Em andamento'), ('Pendente', 'Pendente'), ('Finalizado', 'Finalizado')], max_length=50)),
                ('prazo_inicial_tarefa', models.DateTimeField()),
                ('prazo_final_tarefa', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(auto_now_add=True)),
                ('atribuicao_tarefa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='funcionarios.funcionario')),
            ],
        ),
    ]
