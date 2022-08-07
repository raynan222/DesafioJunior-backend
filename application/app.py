import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from flask_sqlalchemy import SQLAlchemy
from utils.db.db_cidade_estado_populate import Populate
from swagger_ui import api_doc

app = Flask(__name__)
app.config.from_object('config')

api_doc(app, config_path='./utils/swagger.json', url_prefix='/api', title='API doc')

CORS(app)

jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

server = Server(host=os.getenv("BACKEND_HOST", "localhost"), port=os.getenv("PORT", 5000), )
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