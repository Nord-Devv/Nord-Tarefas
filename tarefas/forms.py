from django import forms

from .models import Tarefa


class TarefaAdminForm(forms.ModelForm):
    prazo_inicial_tarefa = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    prazo_final_tarefa = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    class Meta:
        model = Tarefa
        fields = "__all__"
