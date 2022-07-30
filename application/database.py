import os
from flask_sqlalchemy import SQLAlchemy
from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand
from application.app import app

default = 'postgresql://postgres:postgres@localhost/web_app'
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default)
SQLALCHEMY_TRACK_MODIFICATIONS = True
##

app.config["SQLALCHEMY_DATABASE_URI"] = default

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)

server = Server(host="0.0.0.0", port=os.getenv('PORT', 5000))
manager.add_command("runserver", server)
manager.add_command('db', MigrateCommand)