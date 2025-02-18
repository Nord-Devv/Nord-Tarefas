from django.contrib import admin
from django.utils.html import format_html

from .models import Funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = (
        "nome_funcionario",
        "display_foto_funcionario",  # Custom method to display the image
        "sobrenome_funcionario",
        "email_funcionario",
        "descricao_funcionario",
    )

    list_filter = (
        "nome_funcionario",
        "sobrenome_funcionario",
        "email_funcionario",
        "descricao_funcionario",
    )

    def display_foto_funcionario(self, obj):
        if obj.foto_funcionario:
            return format_html(
                '<img src="{}" width="50" height="50" />', obj.foto_funcionario.url
            )
        return "No Image"

    display_foto_funcionario.short_description = "Foto"  # Column header in the admin
