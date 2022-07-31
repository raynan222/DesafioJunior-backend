from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "abc"

CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True)

import Messages
from source.model.acessoTable import Acesso
from source.model.controllerTable import Controller
from source.model.enderecoTable import Endereco
from source.model.estadoTable import Estado
from source.model.loginTable import Login
from source.model.municipioTable import Municipio
from source.model.paisTable import Pais
from source.model.regraTable import Regra
from source.model.usuarioTable import Usuario

from source.controller import authenticationController