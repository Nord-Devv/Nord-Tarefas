from pydantic import BaseModel


class TarefaSchema(BaseModel):
    nome_tarefa: str
    status_tarefa: str
    descricao_tarefa: str | None = None
    atribuicao_tarefa: int
    prazo_inicial_tarefa: str | None = None
    prazo_final_tarefa: str | None = None

    class Config:
        orm_mode = True
