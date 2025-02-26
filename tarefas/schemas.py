from pydantic import BaseModel

from funcionarios.schemas import FuncionarioSchema


class ErrorSchema(BaseModel):
    error: str


class TarefaSchema(BaseModel):
    nome_tarefa: str
    status_tarefa: str
    descricao_tarefa: str | None = None
    atribuicao_tarefa: int | None = None  # Expect an integer (Funcionario ID)
    prazo_inicial_tarefa: str | None = None
    prazo_final_tarefa: str | None = None

    class Config:
        orm_mode = True
