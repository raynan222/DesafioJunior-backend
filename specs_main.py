from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
import json

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
    enderecoList,
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
        spec.tag(dict(name="Rotas", description="Rotas"))

    paths = [
        login,
        acessoView,
        acessoList,
        enderecoView,
        enderecoList,
        enderecoUpdate,
        cadastroLogin,
        loginCreation,
        loginView,
        loginCompleteView,
        loginList,
        loginCompleteList,
        loginUpdate,
        loginCompleteUpdate,
        loginDelete,
        usuarioCreation,
        usuarioView,
        usuarioList,
        usuarioUpdate,
        usuarioDelete,
    ]
    for path in paths:
        spec.path(view=path)

    f = open("utils/out.json", "w")
    f.write(json.dumps(spec.to_dict(), indent=4))
    f.close()
