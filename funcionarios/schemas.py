from ninja import schema


class LoginFuncionarioSchema(schema.Schema):
    email_funcionario: str
    senha_funcionario: str
