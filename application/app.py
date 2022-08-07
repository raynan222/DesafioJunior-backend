import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from flask_sqlalchemy import SQLAlchemy
from utils.db.db_cidade_estado_populate import Populate

app = Flask(__name__)
app.config.from_object('config')

CORS(app)  # Se o deploy for em vpc ou de msm origem, remover cors

jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

server = Server(host=os.getenv("BACKEND_HOST", "backend"), port=os.getenv("PORT", 5000), )
manager.add_command("runserver", server)
manager.add_command("db", MigrateCommand)
manager.add_command("populate", Populate)

import Globals
import source.model
from source.controller import acessoController
from source.controller import authenticationController
from source.controller import enderecoController
from source.controller import loginController
from source.controller import usuarioController
