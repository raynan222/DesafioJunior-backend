import os

REGISTER_SUCCESS_CREATED = "Cadastro de {} criado com sucesso."
REGISTER_SUCCESS_UPDATED = "Cadastro de {} atualizado com sucesso."
REGISTER_SUCCESS_DELETED = "Cadastro de {} excluído com sucesso."
REGISTER_CREATE_INTEGRITY_ERROR = (
    "Não foi possível criar o cadastro. Verifique os dados e tente novamente."
)
REGISTER_CHANGE_INTEGRITY_ERROR = (
    "Não foi possível modificar o cadastro. Verifique os dados e tente novamente."
)
REGISTER_DELETE_INTEGRITY_ERROR = (
    "Não foi possível excluir o cadastro. Verifique os dados e tente novamente."
)
REGISTER_NOT_FOUND = "Cadastro Cod. {} não encontrado no sistema."

AUTH_USER_NOT_FOUND = "O usuário informado não está registrado."
AUTH_USER_PASS_ERROR = "A senha informada não corresponde com a do usuário."
AUTH_USER_DENIED = "O usuário não possui permissão para acessar a URL solicitada."

INVALID_TYPE = "O tipo {} é invalido para esse campo"
INVALID_CPF = "O CPF({}) é invalido."
INVALID_PIS = "O PIS({}) é invalido."
INVALID_EMAIL = "O email({}) é invalido."
USER_INVALID_DELETE = "Não é permitido deletar esse usuário."

ALREADY_EXISTS = "O {} informado já está cadastrado."

TEST_LOGIN = {"email": "raynan@olah.com",
              "senha": "Senha-Secreta",
              "usuario_id": 1,
              "acesso_id": 2}
TEST_USUARIO = {"nome": "Raynan Serafim",
                "pis": "49633872787",
                "cpf": "82848973005",
                "endereco_id": 1}
