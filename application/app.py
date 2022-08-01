from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "abc"
app.config["ROWS_PER_PAGE"] = 10
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

CORS(app) # Se o deploy for em vpc ou de msm origem, remover cors

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True)

import Messages
import source.model
from source.controller import acessoController
from source.controller import authenticationController
from source.controller import enderecoController
from source.controller import loginController
from source.controller import usuarioController
