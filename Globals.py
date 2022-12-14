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
AUTH_USER_SUCCESS = "Login realizado com sucesso."
PASSWORDS_DONT_MATCH = "As senhas não coincidem."
AUTH_USER_DENIED = "O usuário não possui permissão para acessar a URL solicitada."

INVALID_TYPE = "O valor {} é invalido para o campo."
INVALID_CITY = "O municipio selecionado é invalido."
INVALID_CPF = "O CPF é invalido."
INVALID_CEP = "O CEP é invalido."
INVALID_PIS = "O PIS é invalido."
INVALID_EMAIL = "O email é invalido."
EMPTY_FIELD = "O campo {} está vazio."

USER_INVALID_DELETE = "Não é permitido deletar esse usuário."

ALREADY_EXISTS = "O {} informado já está cadastrado."

TEST_LOGIN = {
    "email": "raynan@olah.com",
    "senha": "Senha-Secreta",
    "acesso_id": 2,
    "nome": "Raynan Serafim",
    "pis": "49633872787",
    "cpf": "82848973005",
    "cep": "60869-001",
    "rua": "Oiticicas",
    "numero": "130",
    "bairro": "Cajazeiras",
    "complemento": "Nao tem",
    "municipio_id": 1,
}
