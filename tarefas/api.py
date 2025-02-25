from datetime import datetime

from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware
from ninja import NinjaAPI

from funcionarios.models import Funcionario

from .models import Tarefa
from .schemas import TarefaSchema

api_tarefa = NinjaAPI(urls_namespace="tarefa")


class TarefaAPI:
    @staticmethod
    @api_tarefa.post(
        "/tarefa/adicionar_tarefas", response={200: TarefaSchema, 400: dict}
    )
    def adicionar_tarefa(request, tarefa: TarefaSchema):
        try:
            print("Received tarefa data:", tarefa.model_dump())  # Log the incoming data

            tarefa_data = tarefa.model_dump()

            # Validate if `atribuicao_tarefa` exists
            atribuicao_tarefa_id = tarefa_data.get("atribuicao_tarefa")
            if atribuicao_tarefa_id:
                try:
                    funcionario = Funcionario.objects.get(id=atribuicao_tarefa_id)
                except Funcionario.DoesNotExist:
                    return 400, {
                        "error": f"Funcionario with id {atribuicao_tarefa_id} does not exist."
                    }
            else:
                funcionario = None  # It's optional

            prazo_inicial_tarefa = (
                make_aware(datetime.fromisoformat(tarefa_data["prazo_inicial_tarefa"]))
                if tarefa_data.get("prazo_inicial_tarefa")
                else None
            )
            prazo_final_tarefa = (
                make_aware(datetime.fromisoformat(tarefa_data["prazo_final_tarefa"]))
                if tarefa_data.get("prazo_final_tarefa")
                else None
            )

            # Create the task
            instancia_tarefa = Tarefa.objects.create(
                nome_tarefa=tarefa_data["nome_tarefa"],
                status_tarefa=tarefa_data["status_tarefa"],
                atribuicao_tarefa=funcionario,
                descricao_tarefa=tarefa_data.get("descricao_tarefa", ""),
                prazo_inicial_tarefa=prazo_inicial_tarefa,
                prazo_final_tarefa=prazo_final_tarefa,
            )

            tarefa_dict = model_to_dict(instancia_tarefa)
            # Return the newly created task
            return 200, TarefaSchema.model_validate(tarefa_dict)

        except Exception as e:
            return 400, {"error": str(e)}

    @staticmethod
    @api_tarefa.post(
        "/tarefa/adicionar_tarefas", response={200: TarefaSchema, 400: dict}
    )
    def adicionar_tarefa(request, tarefa: TarefaSchema):
        try:
            print("Received tarefa data:", tarefa.model_dump())  # Log the incoming data

            tarefa_data = tarefa.model_dump()

            # Validate if `atribuicao_tarefa` exists
            atribuicao_tarefa_id = tarefa_data.get("atribuicao_tarefa")
            if atribuicao_tarefa_id:
                try:
                    funcionario = Funcionario.objects.get(id=atribuicao_tarefa_id)
                except Funcionario.DoesNotExist:
                    return 400, {
                        "error": f"Funcionario with id {atribuicao_tarefa_id} does not exist."
                    }
            else:
                funcionario = None  # It's optional

            # Create the task
            instancia_tarefa = Tarefa.objects.create(
                nome_tarefa=tarefa_data["nome_tarefa"],
                status_tarefa=tarefa_data["status_tarefa"],
                atribuicao_tarefa=funcionario,  # Assign the Funcionario object
                descricao_tarefa=tarefa_data.get("descricao_tarefa", ""),
                prazo_inicial_tarefa=tarefa_data.get("prazo_inicial_tarefa"),
                prazo_final_tarefa=tarefa_data.get("prazo_final_tarefa"),
            )

            tarefa_dict = model_to_dict(instancia_tarefa)
            # Return the newly created task
            return 200, TarefaSchema.model_validate(tarefa_dict)

        except Exception as e:
            return 400, {"error": str(e)}

    @staticmethod
    @api_tarefa.delete(
        "/tarefa/remover_tarefa/{nome_tarefa}",
        response={200: TarefaSchema, 404: dict, 400: dict},
    )
    def remover_tarefa(request, nome_tarefa: str):
        try:
            print(f"Deleting task with name: {nome_tarefa}")  # Log the task name
            tarefa = Tarefa.objects.get(nome_tarefa=nome_tarefa)
            print(f"Found task: {tarefa}")  # Log the found task
            tarefa_dict = model_to_dict(tarefa)
            tarefa.delete()
            return 200, TarefaSchema.model_validate(tarefa_dict)
        except Tarefa.DoesNotExist:
            return 404, {"error": f"Tarefa with name '{nome_tarefa}' does not exist."}
        except Exception as e:
            return 400, {"error": str(e)}

    @staticmethod
    @api_tarefa.put(
        "/tarefa/alterar_tarefa/{id_tarefa}", response={200: TarefaSchema, 400: dict}
    )
    def alterar_tarefa(request, id_tarefa: str, dados_tarefa: TarefaSchema):
        try:
            print(f"Updating task with ID: {id_tarefa}")  # Log the task ID
            tarefa = get_object_or_404(Tarefa, id=id_tarefa)
            print(f"Found task: {tarefa}")  # Log the found task

            if dados_tarefa.nome_tarefa is not None:
                tarefa.nome_tarefa = dados_tarefa.nome_tarefa
            if dados_tarefa.status_tarefa is not None:
                tarefa.status_tarefa = dados_tarefa.status_tarefa
            if dados_tarefa.descricao_tarefa is not None:
                tarefa.descricao_tarefa = dados_tarefa.descricao_tarefa
            if dados_tarefa.atribuicao_tarefa is not None:
                funcionario = get_object_or_404(
                    Funcionario, id=dados_tarefa.atribuicao_tarefa
                )
                tarefa.atribuicao_tarefa = funcionario
            if dados_tarefa.prazo_inicial_tarefa is not None:
                tarefa.prazo_inicial_tarefa = make_aware(
                    datetime.fromisoformat(dados_tarefa.prazo_inicial_tarefa)
                )
            if dados_tarefa.prazo_final_tarefa is not None:
                tarefa.prazo_final_tarefa = make_aware(
                    datetime.fromisoformat(dados_tarefa.prazo_final_tarefa)
                )

            tarefa.save()

            tarefa_dict = model_to_dict(tarefa)
            validated_data = TarefaSchema.model_validate(tarefa_dict)

            # Return the validated data
            return 200, validated_data

        except Exception as e:
            # Return a proper error response
            return 400, {"error": str(e)}
