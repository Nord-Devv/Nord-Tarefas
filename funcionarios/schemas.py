from ninja import schema


class LoginFuncionarioSchema(schema.Schema):
    email_usuario: str
    senha_usuario: str
