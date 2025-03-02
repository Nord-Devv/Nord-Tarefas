from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI

from funcionarios.auth import JWTAuth
from funcionarios.models import Funcionario

from .choices import TarefaChoices
from .models import Tarefa
from .schemas import ErrorSchema, StatusUpdateSchema, TarefaSchema

api_tarefa = NinjaAPI(urls_namespace="tarefa", auth=JWTAuth())


class TarefaAPI:
    @staticmethod
    @api_tarefa.get(
        "/listar_tarefas",
        response={200: list[TarefaSchema], 404: ErrorSchema},
        auth=JWTAuth(),
    )
    def listar_tarefas(request):
        user_email = request.auth.get("email_funcionario")
        try:
            funcionario = Funcionario.objects.get(email_funcionario=user_email)
        except Funcionario.DoesNotExist:
            return JsonResponse({"error": "Usuário não encontrado"}, status=404)

        tasks = Tarefa.objects.filter(atribuicao_tarefa=funcionario)

        serialized_tasks = [
            {
                "id": task.id,
                "nome_tarefa": task.nome_tarefa,
                "descricao_tarefa": task.descricao_tarefa,
                "status_tarefa": task.status_tarefa,
                "prazo_inicial_tarefa": task.prazo_inicial_tarefa,
                "prazo_final_tarefa": task.prazo_final_tarefa,
                "foto_funcionario": task.atribuicao_tarefa.foto_funcionario.url
                if task.atribuicao_tarefa.foto_funcionario
                else None,
            }
            for task in tasks
        ]
        return JsonResponse(serialized_tasks, safe=False)

    @staticmethod
    @api_tarefa.delete(
        "/remover_tarefa/{nome_tarefa}",
        response={200: dict, 404: dict, 400: dict},
    )
    def remover_tarefa(request, nome_tarefa: str):
        try:
            print(f"Deleting task with name: {nome_tarefa}")
            tarefa = Tarefa.objects.get(nome_tarefa=nome_tarefa)
            tarefa.delete()
            return 200, {"message": "Task deleted successfully"}
        except Tarefa.DoesNotExist:
            return 404, {"error": f"Tarefa with name '{nome_tarefa}' does not exist."}
        except Exception as e:
            return 400, {"error": str(e)}

    @staticmethod
    @api_tarefa.put(
        "/alterar_status_tarefa/{id_tarefa}", response={200: TarefaSchema, 400: dict}
    )
    def alterar_status_tarefa(request, id_tarefa: int, payload: StatusUpdateSchema):
        try:
            tarefa = get_object_or_404(Tarefa, id=id_tarefa)

            status_validos = [choice[0] for choice in TarefaChoices.CHOICES]
            if payload.novo_status not in status_validos:
                return 400, {
                    "error": f"Status Inválido. Os status válidos são: {status_validos}"
                }

            tarefa.status_tarefa = payload.novo_status
            tarefa.save()

            tarefa_dict = model_to_dict(tarefa)
            if tarefa_dict.get("prazo_inicial_tarefa"):
                tarefa_dict["prazo_inicial_tarefa"] = tarefa_dict[
                    "prazo_inicial_tarefa"
                ].isoformat()
            if tarefa_dict.get("prazo_final_tarefa"):
                tarefa_dict["prazo_final_tarefa"] = tarefa_dict[
                    "prazo_final_tarefa"
                ].isoformat()

            # Validate the data using TarefaSchema
            validacao_data = TarefaSchema.model_validate(tarefa_dict)

            return 200, validacao_data

        except Exception as e:
            return 400, {"error": str(e)}
