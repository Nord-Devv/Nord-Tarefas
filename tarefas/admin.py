from django.contrib import admin

from .models import DeletedTarefa, Tarefa


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = (
        "nome_tarefa",
        "status_tarefa",
        "descricao_tarefa",
        "prazo_inicial_tarefa",
        "prazo_final_tarefa",
    )
    list_filter = (
        "nome_tarefa",
        "status_tarefa",
        "prazo_inicial_tarefa",
        "prazo_final_tarefa",
    )


@admin.register(DeletedTarefa)
class DeletedTarefaAdmin(admin.ModelAdmin):
    list_display = (
        "nome_tarefa",
        "status_tarefa",
        "descricao_tarefa",
        "prazo_inicial_tarefa",
        "prazo_final_tarefa",
    )
    list_filter = (
        "nome_tarefa",
        "status_tarefa",
        "prazo_inicial_tarefa",
        "prazo_final_tarefa",
    )
