import json
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from application.app import app
from source.controller.authenticationController import (
    login,
)
from source.controller.acessoController import (
    acessoView,
    acessoList,
)
from source.model.acessoTable import AcessoModel
from source.controller.enderecoController import (
    enderecoView,
    municipioList,
    enderecoUpdate,
)
from source.model.enderecoTable import EnderecoModel
from source.controller.loginController import (
    cadastroLogin,
    loginCreation,
    loginView,
    loginCompleteView,
    loginList,
    loginCompleteList,
    loginUpdate,
    senhaUpdate,
    loginCompleteUpdate,
    loginDelete,
)
from source.model.loginTable import LoginModel
from source.controller.usuarioController import (
    usuarioCreation,
    usuarioView,
    usuarioList,
    usuarioUpdate,
    usuarioDelete,
)
from source.model.usuarioTable import UsuarioModel

# Script utilizado para gera arquivo de documentação no swagger
# Pode ser acesso em http://localhost:5000/api#/
spec = APISpec(
    title="Backend",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(
        description="API backend para aplicação",
        version="1.0.0-oas3",
        contact=dict(email="raynan.serafim@gmail.com"),
    ),
    servers=[dict(description="Server local", url="http://localhost:5000")],
    tags=[dict(name="Rotas", description="Rotas")],
    plugins=[FlaskPlugin()],
)


jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
spec.components.security_scheme("jwt", jwt_scheme)

with app.app_context():
    models = [
        AcessoModel.schema(),
        EnderecoModel.schema(),
        LoginModel.schema(),
        UsuarioModel.schema(),
    ]
    for model in models:
        spec.components.schema(model["title"], model)

    paths = [
        login,
        acessoView,
        acessoList,
        enderecoView,
        municipioList,
        enderecoUpdate,
        cadastroLogin,
        loginCreation,
        loginView,
        loginCompleteView,
        loginList,
        loginCompleteList,
        loginUpdate,
        loginCompleteUpdate,
        senhaUpdate,
        loginDelete,
        usuarioCreation,
        usuarioView,
        usuarioList,
        usuarioUpdate,
        usuarioDelete,
    ]
    for path in paths:
        spec.path(view=path)

    f = open("utils/swagger.json", "w")
    f.write(json.dumps(spec.to_dict(), indent=4))
    f.close()
