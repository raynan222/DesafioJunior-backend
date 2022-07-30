from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

from source.model.acessoTable import Acesso
from source.model.controllerTable import Controller
from source.model.enderecoTable import Endereco
from source.model.estadoTable import Estado
from source.model.loginTable import Login
from source.model.municipioTable import Municipio
from source.model.paisTable import Pais
from source.model.regraTable import Regra
from source.model.usuarioTable import Usuario
