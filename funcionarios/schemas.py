from ninja import schema
from pydantic import BaseModel


class FuncionarioSchema(BaseModel):
    id: int
    nome_funcionario: str
    email_funcionario: str
    # Add other fields as needed

    class Config:
        orm_mode = True


class LoginFuncionarioSchema(schema.Schema):
    email_funcionario: str
    senha_funcionario: str
